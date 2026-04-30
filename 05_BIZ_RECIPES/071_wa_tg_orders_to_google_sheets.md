---
title: WhatsApp/Telegram заказы → Google Sheets — автосбор без ручного ввода
tags: #biz_recipe #whatsapp #telegram #n8n #google_sheets #orders #automation
source: yt_0fz1MIvdV1s
date: 2026-04-29
score: Pain=8 Dev=8 Profit=7 ИТОГ=23
---

### 1. Описание идеи

Малый бизнес принимает заказы в WhatsApp или Telegram: клиент пишет «хочу 2 пиццы Маргарита и 1 Пепперони, адрес: ул. Ленина 5». Менеджер вручную переносит это в таблицу. n8n + AI парсит сообщение автоматически и добавляет структурированную строку в Google Sheets.

Сохраняет 3–5 часов/день при объёме от 30+ заказов.

### 2. Технический стек

- n8n (Webhook или Telegram/WhatsApp Trigger)
- Telegram Bot API / WhatsApp Cloud API (Meta)
- Claude API или GPT (парсинг текста заказа в JSON)
- Google Sheets API v4 (запись строки)
- OAuth2 Google

### 3. Пошаговый план внедрения

**Шаг 1 — Telegram-бот для приёма заказов**
```
@BotFather → /newbot → получить TOKEN
n8n → Telegram Trigger нода → вставить TOKEN
```

**Шаг 2 — AI-парсинг заказа**
```
HTTP Request → Claude API:
System: "Ты — парсер заказов. Из текста извлеки:
  items (массив: name, qty, price если есть),
  address (строка или null),
  phone (строка или null),
  comment (прочее).
  Верни только JSON."
User: "{{$json.message.text}}"
```

**Пример входа/выхода:**
```
Вход:  "2 пиццы Маргарита и 1 Пепперони, адрес Ленина 5, тел 79001234567"
Выход: {
  "items": [
    {"name": "Маргарита", "qty": 2},
    {"name": "Пепперони", "qty": 1}
  ],
  "address": "ул. Ленина 5",
  "phone": "+79001234567",
  "comment": null
}
```

**Шаг 3 — Запись в Google Sheets**
```
Google Sheets нода → Append Row:
Spreadsheet: [ID таблицы]
Sheet: Заказы
Values:
  A: {{$now.toFormat('dd.MM.yyyy HH:mm')}}   // дата/время
  B: {{$json.message.from.first_name}}         // клиент
  C: {{$json.parsed.phone}}
  D: {{$json.parsed.address}}
  E: {{JSON.stringify($json.parsed.items)}}    // товары
  F: "Новый"                                   // статус
```

**Шаг 4 — Подтверждение клиенту**
```
Telegram нода → Send Message:
chat_id: {{$json.message.chat.id}}
text: "✅ Заказ принят! Ожидайте подтверждения в течение 5 минут."
```

### 4. Сценарии использования

| Бизнес | Канал | Что парсим |
|---|---|---|
| Пиццерия / доставка еды | Telegram | Блюда, адрес, телефон |
| Цветочный магазин | WhatsApp | Состав букета, дата, адрес |
| Интернет-магазин одежды | Telegram | Артикул, размер, цвет, адрес |
| Строительные материалы | WhatsApp | Товар, количество, объект |

### 5. Нюансы

- Клиенты пишут по-разному — AI-парсинг справляется с неструктурированным текстом лучше regex
- WhatsApp Cloud API требует верификации бизнеса в Meta (1–5 дней)
- Для WhatsApp Business (обычный, не API) — используют EvoAPI или WA-шлюзы
- Google Sheets лимит: 100 запросов/100 сек — при высоком трафике добавить буферную очередь

### 6. Оценка эффективности

- Сложность: 2/5
- Время внедрения: 1–2 дня
- ROI: при 50 заказах/день × 3 мин ручного ввода = 2.5 часа/день экономии; окупаемость — неделя
