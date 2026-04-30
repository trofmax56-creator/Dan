---
title: AI Telegram-бот через n8n — настройка за 7 минут без кода
tags: #biz_recipe #n8n #telegram #ai #chatbot #claude #openai #nocode
source: yt_VQEpvwHFhzI
date: 2026-04-29
score: Pain=8 Dev=9 Profit=7 ИТОГ=24
---

### 1. Описание идеи

Самый быстрый способ запустить AI-чатбот в Telegram для бизнеса: n8n Webhook + Telegram Bot API + Claude/GPT API. Бот принимает сообщение, передаёт в LLM с системным промптом компании, возвращает ответ. Без написания кода, без сервера — только n8n.cloud и BotFather.

Применение: FAQ-бот для клиентов, бот поддержки, квалификатор лидов, внутренний помощник команды.

### 2. Технический стек

- Telegram Bot API (BotFather — бесплатно)
- n8n (n8n.cloud бесплатный тариф или self-hosted)
- Claude API (`claude-haiku-4-5-20251001` — дёшево) или OpenAI GPT-3.5
- Webhook нода в n8n — принимает сообщения от Telegram
- HTTP Request нода — вызов LLM API и отправка ответа

### 3. Пошаговый план внедрения

**Шаг 1 — Создать бота (2 мин)**
```
Telegram → @BotFather → /newbot
→ Задать имя и username (например, @MyCompanyBot)
→ Скопировать токен: 1234567890:AAF_xxx...
```

**Шаг 2 — Настроить Webhook в n8n (2 мин)**
```
n8n → New Workflow → Add Node → Webhook
→ HTTP Method: POST
→ Скопировать Webhook URL (вида https://xxx.n8n.cloud/webhook/abc123)

Telegram → зарегистрировать Webhook:
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<N8N_WEBHOOK_URL>"
```

**Шаг 3 — Получить текст сообщения (1 мин)**
```javascript
// Set нода или Expression
{{$json.message.text}}          // текст сообщения
{{$json.message.chat.id}}       // chat_id для ответа
{{$json.message.from.first_name}} // имя пользователя
```

**Шаг 4 — Вызов LLM (1 мин)**
```
HTTP Request нода:
URL: https://api.anthropic.com/v1/messages
Method: POST
Headers:
  x-api-key: sk-ant-xxx
  anthropic-version: 2023-06-01
  Content-Type: application/json
Body:
{
  "model": "claude-haiku-4-5-20251001",
  "max_tokens": 512,
  "system": "Ты — помощник компании [Название]. Отвечай кратко и по делу. [FAQ компании]",
  "messages": [{"role": "user", "content": "{{$json.message.text}}"}]
}
```

**Шаг 5 — Отправить ответ в Telegram (1 мин)**
```
HTTP Request нода:
URL: https://api.telegram.org/bot<TOKEN>/sendMessage
Method: POST
Body:
{
  "chat_id": "{{$('Webhook').item.json.message.chat.id}}",
  "text": "{{$json.content[0].text}}"
}
```

**Итого — 7 минут. Activate Workflow → тестируем.**

### 4. Сценарии использования

| Бизнес | Системный промпт | Польза |
|---|---|---|
| Клиника | Расписание врачей, FAQ о процедурах | Запись без звонка |
| Интернет-магазин | Статусы заказов, FAQ | Снижение нагрузки на поддержку |
| Агентство | Прайс, портфолио, кейсы | Квалификация лидов 24/7 |
| Внутренний | Регламенты, инструкции HR | Ответы сотрудникам без HR |

### 5. Нюансы

- Telegram требует HTTPS для Webhook — n8n.cloud даёт его автоматически
- Claude Haiku стоит ~$0.00025 за 1000 токенов — 1000 сообщений ≈ $0.15
- Для сохранения контекста диалога нужно хранить историю (Google Sheets / Redis) — без этого бот «забывает» предыдущие сообщения
- Polling (альтернатива Webhook) проще, но медленнее — только для тестов

### 6. Оценка эффективности

- Сложность: 1/5
- Время внедрения: 7–30 минут
- ROI: один бот заменяет 20–30% обращений в поддержку; экономия от ₽15 000/мес при одном операторе поддержки
