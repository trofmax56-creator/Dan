---
title: n8n Telegram-бот с ИИ — полная настройка с памятью и внешними данными
tags: #biz_recipe #n8n #telegram #ai #chatbot #memory #claude #integration
source: yt_uckxNqMM6UQ
date: 2026-04-29
score: Pain=8 Dev=8 Profit=7 ИТОГ=23
---

### 1. Описание идеи

Расширенная версия AI Telegram-бота: с памятью диалога (контекст не теряется), подключением внешних источников данных (Google Sheets, CRM, база знаний) и маршрутизацией сложных запросов к живому менеджеру. Отличие от рецепта 069: не просто Q&A, а полноценный агент.

### 2. Технический стек

- n8n (Telegram Trigger + HTTP Request + Memory ноды)
- Telegram Bot API
- Claude API (основная модель) или OpenAI GPT
- Google Sheets / Notion — база знаний и история диалогов
- Bitrix24 / amoCRM — данные о клиентах и заказах
- Simple Memory нода n8n (встроенная в n8n v1.x)

### 3. Пошаговый план внедрения

**Шаг 1 — Создать бота и базовый Webhook**
```
@BotFather → /newbot → TOKEN
n8n → Telegram Trigger → вставить TOKEN
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<N8N_URL>"
```

**Шаг 2 — Сохранение истории диалога**
```javascript
// Использовать n8n Simple Memory или Google Sheets
// Ключ: chat_id пользователя

// Google Sheets структура:
// chat_id | role | message | timestamp

// При каждом сообщении:
// 1. Считать последние N строк для этого chat_id
// 2. Сформировать messages[] для Claude
// 3. После ответа — добавить обе строки (user + assistant)

const history = await sheets.getRows({ filter: `chat_id = ${chat_id}`, limit: 10 })
const messages = history.map(r => ({ role: r.role, content: r.message }))
messages.push({ role: "user", content: incoming_text })
```

**Шаг 3 — Подключение базы знаний**
```javascript
// Перед вызовом Claude — найти релевантные данные
// (простой поиск по ключевым словам в Google Sheets / Notion)
const kb = await sheets.search("FAQ", incoming_text)
const context = kb.length > 0 ? `Используй эти данные:\n${kb.join('\n')}` : ""

// Claude системный промпт:
const system = `
Ты — помощник компании [Название]. ${context}
Отвечай только на основе предоставленных данных.
Если не знаешь — скажи "Уточню у менеджера" и создай задачу.
`
```

**Шаг 4 — Эскалация к менеджеру**
```javascript
// Если бот не знает ответа или клиент просит менеджера:
if (response.includes("Уточню у менеджера") || incoming_text.includes("менеджер")) {
  // Telegram: уведомить менеджера
  await telegram.sendMessage(MANAGER_CHAT_ID,
    `❓ Клиент ${user_name} (${chat_id}) просит помощи:\n"${incoming_text}"`)
  // CRM: создать задачу
  await bitrix24.task.add({ title: `Запрос из Telegram: ${user_name}` })
}
```

**Шаг 5 — Команды бота**
```
/start  → приветствие + краткое меню
/help   → список возможностей
/status → статус заказа (запрос в CRM по номеру телефона)
/reset  → очистить историю диалога
```

### 4. Сценарии использования

| Функция | Источник данных | Пример |
|---|---|---|
| FAQ | Google Sheets «База знаний» | «Как долго доставка?» |
| Статус заказа | Bitrix24 CRM по телефону | «Где мой заказ #1234?» |
| Запись на услугу | Google Calendar API | «Запишите меня на 15 мая» |
| Прайс-лист | Google Sheets «Товары» | «Сколько стоит X?» |

### 5. Нюансы

- Memory нода n8n v1.x встроена — использовать её вместо Google Sheets, если не нужна долгосрочная история
- История диалога = N последних сообщений. Слишком длинный контекст → дороже и медленнее. Оптимум: 10–20 сообщений
- Для проверки Telegram Webhook: `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
- При использовании polling (альтернатива Webhook) — бот отвечает с задержкой 1–3 сек

### 6. Оценка эффективности

- Сложность: 2/5
- Время внедрения: 2–4 дня
- ROI: бот с памятью закрывает 40–60% типовых обращений без участия менеджера
