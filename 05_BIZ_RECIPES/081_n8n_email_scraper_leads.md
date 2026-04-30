---
title: n8n — автосбор email-адресов с сайтов для лидогенерации
tags: #biz_recipe #n8n #scraping #leads #email #crm #automation
source: yt_XMYuEIje7_g
date: 2026-04-29
score: Pain=7 Dev=8 Profit=7 ИТОГ=22
---

### 1. Описание идеи

Вместо ручного поиска контактов на сайтах — n8n автоматически скачивает HTML страниц, извлекает email-адреса через regex/CSS-селекторы, валидирует их и добавляет в CRM или Google Sheets для дальнейшего контакта. Подходит для лидогенерации по нишевым каталогам и агрегаторам.

### 2. Технический стек

- n8n (HTTP Request + Code Node)
- Regex / CSS-селекторы — парсинг email из HTML
- Hunter.io API / Zerobounce API — верификация email
- Google Sheets API — хранение результатов
- Bitrix24 / amoCRM API — создание контактов
- Proxy (опционально) — обход блокировок

### 3. Пошаговый план внедрения

**Шаг 1 — Получить список URL для парсинга**
```
Google Sheets: url | company | status
Заполнить: список сайтов компаний-ЦА (из 2GIS, Яндекс.Карты, отраслевых каталогов)
```

**Шаг 2 — Скачать HTML страницы**
```javascript
// n8n: читать URL из Sheets → HTTP Request нода
GET {{url}}
Headers:
  User-Agent: Mozilla/5.0 (compatible; GoogleBot/2.1)
// Получить: body (HTML-контент)
```

**Шаг 3 — Извлечь email из HTML**
```javascript
// Code нода (JavaScript)
const html = $input.item.json.body

// Метод 1: regex (простой, быстрый)
const emailRegex = /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g
const emails = [...new Set(html.match(emailRegex) || [])]

// Метод 2: CSS-селектор для mailto:
// Если n8n имеет cheerio: $('a[href^="mailto:"]').map((_, el) => $(el).attr('href').replace('mailto:',''))

// Фильтрация: убрать мусор
const filtered = emails.filter(e =>
  !e.includes('example.com') &&
  !e.includes('noreply') &&
  !e.includes('sentry') &&
  e.split('@')[1].split('.').pop().length >= 2
)

return filtered.map(email => ({ email, source_url: $input.item.json.url }))
```

**Шаг 4 — Верификация email**
```javascript
// HTTP Request → Hunter.io Email Verifier
GET https://api.hunter.io/v2/email-verifier
Params: email={{email}}&api_key={{hunter_key}}
// Результат: {status: "valid|invalid|risky|unknown", score: 0-100}

// Оставлять только status="valid" и score > 70
```

**Шаг 5 — Сохранить в Google Sheets / CRM**
```
Sheets: email | company | source_url | verified | date_added | status(new)
CRM: crm.contact.add { EMAIL: email, COMPANY_TITLE: company, SOURCE: "Парсинг" }
```

### 4. Сценарии использования

| Источник URL | Тип парсинга | Применение |
|---|---|---|
| 2GIS / Яндекс.Карты (экспорт) | Страница компании → email | Холодный outreach |
| Отраслевой каталог | Список участников → email | Партнёрские рассылки |
| LinkedIn (публичные) | Профиль → контакт | B2B outreach |
| Habr / VC.ru авторы | Профиль → email | Контент-партнёрство |

### 5. Нюансы

- Для JS-рендерируемых сайтов (React/Vue) простой HTTP Request не работает → нужен Puppeteer нода n8n
- Сайты могут блокировать парсинг по User-Agent или IP → менять User-Agent, использовать паузы, прокси
- Hunter.io: 50 верификаций/мес бесплатно. При объёме → Zerobounce или NeverBounce ($0.003/email)
- Законодательство: сбор email с сайтов — серая зона. Добавлять unsubscribe в письма, соблюдать 152-ФЗ

### 6. Оценка эффективности

- Сложность: 2/5
- Время внедрения: 1–3 дня
- ROI: ручной поиск 1 email — 3–10 мин. n8n — 100 email за 5–10 мин автоматически
