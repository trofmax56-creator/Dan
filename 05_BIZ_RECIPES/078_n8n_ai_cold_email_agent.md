---
title: n8n + Claude — AI-агент полного цикла холодных писем
tags: #biz_recipe #n8n #email #cold_outreach #claude #sales #automation #crm
source: yt_yWTk2cPsn98
date: 2026-04-29
score: Pain=8 Dev=7 Profit=8 ИТОГ=23
---

### 1. Описание идеи

Полностью автоматизированный цикл холодных писем: агент берёт список контактов из Google Sheets, генерирует персонализированное письмо под каждого через Claude (с учётом компании, должности, отрасли), отправляет через Gmail/SendGrid, отслеживает ответы и автоматически создаёт сделки в CRM при положительной реакции.

Конверсия персонализированных AI-писем — в 3–4 раза выше шаблонных.

### 2. Технический стек

- n8n — оркестратор
- Google Sheets — база контактов (name, email, company, industry, title, context)
- Claude API — генерация персонального письма
- Gmail API / SendGrid API — отправка
- Gmail Trigger — отслеживание входящих ответов
- Bitrix24 / amoCRM API — создание сделки при положительном ответе
- Webhook (SendGrid Events) — трекинг открытий

### 3. Пошаговый план внедрения

**Шаг 1 — Подготовка базы контактов**
```
Google Sheets колонки:
name | company | title | email | industry | pain_point | status | sent_date | last_reply

Минимум для персонализации: name + company + title
Лучше добавить: последняя новость компании, tech stack, боль
```

**Шаг 2 — Генерация персонального письма**
```javascript
// Schedule Trigger (пн-пт 09:00) → читает строки со status="new"
// HTTP Request → Claude API

const letter = await claude({
  system: `Ты — опытный B2B sales-менеджер.
  Пишешь холодное письмо от имени компании [Название].
  Продукт: [описание].
  Стиль: короткое (3-4 предложения), конкретное, без воды.
  Персонализация: упомяни должность, компанию или боль.
  Закончи CTA: предложи 15-минутный звонок.`,
  user: `Получатель: ${name}, ${title}, компания ${company} (${industry}).
  Контекст: ${pain_point || "нет"}.
  Напиши subject и body письма. Верни JSON {subject, body}.`
})
```

**Шаг 3 — Отправка через Gmail API**
```javascript
// HTTP Request → Gmail API
POST https://gmail.googleapis.com/gmail/v1/users/me/messages/send
Headers: { Authorization: "Bearer {{oauth_token}}" }
Body:
{
  "raw": "{{base64_encode(
    'To: ' + email + '\r\n' +
    'Subject: ' + subject + '\r\n' +
    'Content-Type: text/plain; charset=utf-8\r\n\r\n' +
    body
  )}}"
}

// Обновить в Google Sheets: status="sent", sent_date={{today}}
```

**Шаг 4 — Отслеживание ответов**
```javascript
// n8n Gmail Trigger: New Email в папке "Входящие"
// Проверить: sender email совпадает с кем-то в базе?

// HTTP Request → Claude API: оценить тональность ответа
const reaction = await claude({
  system: "Определи реакцию на cold email. Верни JSON: {intent: positive|neutral|negative|ooo, summary: ''}",
  user: reply_text
})

// Если positive:
// → amoCRM / Bitrix24: создать сделку STAGE="Переговоры"
// → Telegram: "✅ Горячий лид: ${name} (${company}) ответил!"
// → Google Sheets: status="replied_positive"
```

**Шаг 5 — Follow-up цепочка**
```
Schedule Trigger → проверить записи где:
  status="sent" AND sent_date < (today - 3 дня) AND status != "replied"

→ Отправить follow-up письмо (более короткое, другой angle)
→ Максимум 3 follow-up, потом status="cold"
```

### 4. Сценарии использования

| Цель кампании | Claude prompt акцент | CTA |
|---|---|---|
| Назначить демо | Конкретная боль + как решаем | «15 минут звонка?» |
| Партнёрство | Взаимная выгода | «Обсудим синергию?» |
| Реактивация | Новая функция / кейс | «Что изменилось у нас» |
| Event-invite | Эксклюзивность | «Место только для вас» |

### 5. Нюансы

- Google Workspace аккаунт нужен для Gmail API (обычный Gmail — ограничен)
- SendGrid лучше для больших объёмов: трекинг открытий + аналитика + репутация IP
- Claude генерирует уникальный текст для каждого контакта — это критично для прохождения спам-фильтров
- Лимит: не более 50–100 писем/день с одного ящика (репутация домена)

### 6. Оценка эффективности

- Сложность: 3/5
- Время внедрения: 4–6 дней
- ROI: персонализированные AI-письма дают 3–4x выше open rate vs шаблонные; один SDR = 30 писем/день → агент = 200+/день
