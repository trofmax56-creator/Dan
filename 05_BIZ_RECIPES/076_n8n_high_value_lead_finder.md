---
title: n8n — автоматический поиск высокоценных лидов с обогащением данных
tags: #biz_recipe #n8n #leads #apollo #hunter #enrichment #ai #crm
source: yt_ebAzlBAsxrU
date: 2026-04-29
score: Pain=8 Dev=7 Profit=8 ИТОГ=23
---

### 1. Описание идеи

Из входящего потока лидов (формы, парсинг, купленные базы) автоматически выделяются «высокоценные» по критериям: должность Decision Maker, размер компании, отрасль, бюджет. Система обогащает данные через Apollo.io / Clearbit, оценивает через Claude и передаёт только квалифицированных в CRM для немедленной работы менеджера.

### 2. Технический стек

- n8n — оркестратор
- Apollo.io API / Hunter.io API / Clearbit API — обогащение данных о компании и контакте
- Claude API — финальная квалификация по критериям идеального клиента
- Bitrix24 / amoCRM API — создание сделки для горячих лидов
- Google Sheets — источник сырых лидов и лог отфильтрованных
- Telegram Bot — алерты о горячих лидах

### 3. Пошаговый план внедрения

**Шаг 1 — Определить профиль идеального клиента (ICP)**
```
Вместе с клиентом заполнить:
✓ Отрасли: [IT, производство, ритейл...]
✓ Размер компании: [50–500 сотрудников]
✓ Должность: [CEO, CMO, Head of Sales, ИТ-директор]
✓ Бюджет: [от ₽500k в год]
✓ Регион: [Москва, СПб, РФ]
```

**Шаг 2 — Обогащение данных через Apollo.io**
```javascript
// HTTP Request → Apollo.io People Match API
POST https://api.apollo.io/v1/people/match
Headers: { "X-Api-Key": "{{apollo_key}}" }
Body: { "email": "{{lead.email}}", "reveal_personal_emails": true }

// Получаем:
// title, organization.name, organization.num_employees,
// organization.industry, organization.estimated_annual_revenue
```

**Шаг 3 — Скоринг через Claude**
```javascript
const score = await claude({
  system: `Ты — эксперт B2B квалификации. ICP компании:
  - Отрасли: ${ICP.industries}
  - Размер: ${ICP.size}
  - Должности: ${ICP.titles}
  - Бюджет: ${ICP.budget}
  
  Оцени лида. Верни JSON:
  { score: 0-100, tier: "hot|warm|cold", match_reasons: [], disqualifiers: [] }`,
  user: JSON.stringify(enriched_lead)
})
```

**Шаг 4 — Маршрутизация по результату**
```javascript
// Switch нода по score
score >= 70 (hot):
  → amoCRM: создать сделку STAGE="Переговоры", PRIORITY=HIGH
  → Telegram: "🔥 Горячий лид: ${name}, ${company} — ${title}"

score 40-69 (warm):
  → amoCRM: создать контакт, поставить в очередь нагрева
  → Email: автоматическое письмо с кейсами

score < 40 (cold):
  → Google Sheets: архив. Не тратить время менеджера
```

**Шаг 5 — Логирование метрик**
```
Google Sheets: timestamp | email | company | title | apollo_score | claude_tier | action
→ Еженедельный отчёт: конверсия hot → meeting
```

### 4. Сценарии использования

| Источник лидов | Метод обогащения | Результат |
|---|---|---|
| Форма сайта | Clearbit по email | Мгновенная квалификация |
| Парсинг 2GIS / LinkedIn | Apollo.io | Отсев нецелевых |
| Купленная база | Hunter.io verify + Apollo | Очистка + скоринг |
| Вебинарная регистрация | Clearbit + Claude | Приоритизация follow-up |

### 5. Нюансы

- Apollo.io: бесплатный план 50 запросов/мес. Платный от $49/мес
- Clearbit → теперь HubSpot Breeze. Альтернатива в РФ: Контур.Фокус API (ИНН → реквизиты, выручка)
- Комбинация ИНН + Контур.Фокус даёт данные о российских компаниях точнее Apollo
- Claude оценивает комплексно — учитывает контекст, а не только формальные поля

### 6. Оценка эффективности

- Сложность: 3/5
- Время внедрения: 4–6 дней
- ROI: менеджер работает только с hot-лидами (25–30% от потока) → конверсия × 3–4 при том же времени
