---
title: Browser AI — парсинг цен конкурентов → авто-обновление прайса в МойСклад через n8n
tags: #biz_recipe #automation #moysklad #n8n #parsing #action_needed
---

### 1. Описание идеи
Browser AI (или Firecrawl) автоматически обходит страницы конкурентов по расписанию, извлекает цены и номенклатуру, сравнивает с текущим прайсом в МойСклад. При отклонении > X% — создаёт задачу на пересмотр цены или обновляет прайс автоматически.

### 2. Технический стек
- AI: Claude API (для нормализации и сравнения данных) / Browser AI (парсинг)
- CRM/ERP: МойСклад (REST API)
- Middleware: n8n (self-hosted)

### 3. Пошаговый план внедрения
1. В n8n создать Schedule-триггер (каждый день в 07:00)
2. HTTP Request node → Firecrawl API: передать URL страниц конкурентов (список хранить в переменной n8n)
3. Claude API node: system = "Извлеки таблицу: артикул, название, цена. JSON-массив."; user = html-текст страницы
4. HTTP Request → МойСклад `GET /entity/product` — получить текущие цены
5. Function node: сравнить цены, найти расхождения > 10%
6. Ветка A (авто): МойСклад `PUT /entity/product/{id}` — обновить `salePrices`
7. Ветка B (задача): Bitrix24 `tasks.task.add` — создать задачу коммерческому директору

### 4. Промпты и Код
```
SYSTEM:
Ты — парсер данных. Из HTML-текста страницы извлеки все товарные позиции.
Верни JSON-массив: [{"sku": "...", "name": "...", "price": 0}].
Если артикул отсутствует — используй первые 6 символов названия как sku.
Числа без пробелов и валюты. Если цена не найдена — price: null.
```

```js
// n8n Function node — сравнение цен
const competitors = $input.first().json.parsed_prices; // от Claude
const current = $input.last().json.moysklad_prices;   // от МойСклад

const threshold = 0.10; // 10%

return competitors
  .map(c => {
    const existing = current.find(m => m.sku === c.sku);
    if (!existing || c.price === null) return null;
    const diff = (c.price - existing.price) / existing.price;
    if (Math.abs(diff) > threshold) {
      return { sku: c.sku, competitor_price: c.price, our_price: existing.price, diff_pct: (diff * 100).toFixed(1), id: existing.id };
    }
    return null;
  })
  .filter(Boolean);
```

```json
// МойСклад — обновление цены продажи
// PUT https://api.moysklad.ru/api/remap/1.2/entity/product/{id}
{
  "salePrices": [
    {
      "value": 150000,
      "currency": { "meta": { "href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/RUB_ID", "type": "currency" } },
      "priceType": { "meta": { "href": "https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/SALE_ID", "type": "pricetype" } }
    }
  ]
}
```

### 5. Оценка эффективности
- Сложность: 3/5
- ROI: исключает ручной мониторинг (~2 ч/нед аналитика); цены всегда актуальны → меньше потерь маржи

**Ссылки:** [[02_TOOLS/MoySklad_API]] | [[02_TOOLS/n8n_setup]] | [[03_GUIDES/firecrawl_parsing]]
