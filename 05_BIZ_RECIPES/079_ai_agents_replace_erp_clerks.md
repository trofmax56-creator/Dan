---
title: AI-агенты вместо ERP-клерков — автоматизация документооборота в 1С/Bitrix24
tags: #biz_recipe #ai #erp #1c #bitrix24 #automation #documents #ocr #n8n
source: yt_3R1p64QOPrY
date: 2026-04-29
score: Pain=8 Dev=5 Profit=9 ИТОГ=22
---

### 1. Описание идеи

ERP-клерк вручную обрабатывает входящие документы: счета, накладные, акты → вводит данные в 1С / Bitrix24. AI-агент делает это автоматически: получает PDF/фото документа, распознаёт реквизиты через OCR+LLM, создаёт запись в системе. Точность — до 98%, скорость — секунды вместо минут.

### 2. Технический стек

- Document Intelligence / OCR: Яндекс OCR API, Tesseract, Azure Form Recognizer
- Claude API / GPT-4 Vision — структурирование данных из распознанного текста
- n8n / Make.com — оркестрация
- Email Trigger (IMAP) / Telegram Bot — приём документов
- 1С REST API / Bitrix24 API — создание записей
- Google Drive — хранение оригиналов

### 3. Пошаговый план внедрения

**Шаг 1 — Канал приёма документов**
```
Вариант А: Email (бухгалтерия присылает PDF)
  n8n → Email Trigger (IMAP) → Extract Attachments

Вариант Б: Telegram-бот (фото документа с телефона)
  n8n → Telegram Trigger → получить photo file_id
  → HTTP Request → Telegram API → скачать файл
```

**Шаг 2 — OCR + структурирование**
```javascript
// Вариант 1: Яндекс Vision API (для русских документов — лучше)
POST https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze
Body: {
  "folderId": "{{folder_id}}",
  "analyze_specs": [{ "content": "{{base64_image}}", "features": [{"type": "TEXT_DETECTION"}] }]
}

// Вариант 2: GPT-4 Vision / Claude Vision (если документ сложный)
// → Загрузить image как base64 или URL
// → Промпт: "Извлеки из документа: тип, дата, номер, поставщик ИНН, сумма, НДС, позиции"
```

**Шаг 3 — Claude: нормализация и проверка**
```javascript
const result = await claude({
  system: `Ты — бухгалтерский ассистент. Нормализуй данные документа.
  Исправь форматы: дата → YYYY-MM-DD, сумма → число без пробелов, ИНН → 10/12 цифр.
  Если поле непонятно — null. Верни JSON строго по схеме:
  { type, date, number, supplier: {name, inn, kpp}, total, vat, items: [{name, qty, price}] }`,
  user: ocr_text
})
```

**Шаг 4 — Создание записи в 1С / Bitrix24**
```javascript
// Если тип = "Счёт" → Bitrix24
await bitrix24.deal.add({ TITLE: `Счёт ${doc.number}`, OPPORTUNITY: doc.total })

// Если тип = "Накладная" → 1С
await fetch("http://1c-server/base/hs/documents/create", {
  method: "POST",
  body: JSON.stringify({ type: "ПоступлениеТоваров", data: doc })
})

// Сохранить оригинал в Google Drive
await drive.upload(file, `Документы/${doc.date}/${doc.number}.pdf`)
```

**Шаг 5 — Уведомление об исключениях**
```javascript
// Если confidence < 80% или ИНН не прошёл проверку:
await telegram.sendMessage(ACCOUNTANT_CHAT_ID,
  `⚠️ Документ ${filename} требует проверки. Ошибка: ${error}`)
```

### 4. Сценарии использования

| Документ | OCR задача | Действие |
|---|---|---|
| Входящий счёт | Реквизиты, сумма | Создать приходный ордер в 1С |
| Товарная накладная | Позиции, количество | Оприходование товара в 1С |
| Акт выполненных работ | Стороны, сумма, дата | Сделка «Закрыта» в Bitrix24 |
| Договор | Контрагент, сроки | Контакт + напоминание в CRM |

### 5. Нюансы

- Яндекс Vision API лучше Azure для русских рукописей и нестандартных шрифтов
- Качество OCR критично зависит от качества сканирования. Рекомендовать клиенту: 300 DPI, цвет
- Для 1С нужно разработать HTTP-сервис в конфигуратора (или использовать готовое расширение)
- Проверять ИНН через ОГРН API (nalog.ru) — исключает ошибки ввода

### 6. Оценка эффективности

- Сложность: 4/5
- Время внедрения: 10–15 дней
- ROI: обработка 1 документа вручную — 3–10 мин. Агент — 10–30 сек. При 100 документах/день → 5–15 часов/день экономии (1 FTE клерка)
