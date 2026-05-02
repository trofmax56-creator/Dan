---
title: МойСклад + Claude — семантическое сопоставление артикулов поставщиков
tags: #biz_recipe #automation #moysklad #claude_code #action_needed
---

### 1. Описание идеи
Разные поставщики называют одну позицию по-разному: "Болт М8×40 DIN933" у одного, "Болт шестигр. М8 L40" у другого. Claude через семантический поиск сопоставляет артикулы из прайса поставщика с номенклатурой МойСклад, предлагает связку с confidence-score. Менеджер подтверждает только спорные случаи — рутинный матчинг уходит в автомат.

### 2. Технический стек
- AI: Claude API (claude-sonnet-4-6) + embeddings (опционально: OpenAI text-embedding-3-small)
- CRM/ERP: МойСклад (REST API)
- Middleware: Python-скрипт / n8n

### 3. Пошаговый план внедрения
1. Получить прайс поставщика (Excel/CSV) → распарсить в JSON `[{sku, name, price}]`
2. GET `https://api.moysklad.ru/api/remap/1.2/entity/product?limit=1000` — выгрузить номенклатуру МойСклад
3. Батчами по 20 позиций передавать в Claude API (промпт ниже): поставщик → МойСклад, вернуть JSON с `match_id` и `confidence`
4. Позиции с `confidence >= 0.85` — авто-связать через `PUT /entity/product/{id}` (обновить поле `article` или `supplierCode`)
5. Позиции с `confidence < 0.85` — создать CSV-отчёт для ручной проверки менеджером
6. (Опция) Новые позиции без совпадений — создать черновик товара через `POST /entity/product`

### 4. Промпты и Код
```
SYSTEM:
Ты — системный матчер номенклатуры. Твоя задача — найти соответствие между позициями поставщика
и позициями из базы МойСклад.

Для каждой позиции поставщика верни JSON:
{"supplier_sku": "...", "supplier_name": "...", "match_id": "UUID или null", "match_name": "...", "confidence": 0.0–1.0}

confidence: 1.0 — точное совпадение, 0.7–0.99 — вероятное, < 0.7 — сомнительно.
Если совпадения нет — match_id: null, confidence: 0.

USER:
Позиции поставщика:
{supplier_batch_json}

База МойСклад (первые 200 позиций):
{moysklad_catalog_json}
```

```python
import anthropic, json, math

client = anthropic.Anthropic()

def match_batch(supplier_items: list, moysklad_catalog: list) -> list:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Позиции поставщика:\n{json.dumps(supplier_items, ensure_ascii=False)}\n\nБаза МойСклад:\n{json.dumps(moysklad_catalog, ensure_ascii=False)}"
        }]
    )
    return json.loads(response.content[0].text)

def process_all(supplier: list, catalog: list, batch_size=20) -> list:
    results = []
    for i in range(0, len(supplier), batch_size):
        batch = supplier[i:i+batch_size]
        results.extend(match_batch(batch, catalog))
    return results

# Разделение результатов
matched = [r for r in results if r["confidence"] >= 0.85]
review  = [r for r in results if r["confidence"] < 0.85]
```

```python
# Авто-обновление supplierCode в МойСклад
import requests

HEADERS = {"Authorization": f"Bearer {MOYSKLAD_TOKEN}", "Content-Type": "application/json"}

for item in matched:
    requests.put(
        f"https://api.moysklad.ru/api/remap/1.2/entity/product/{item['match_id']}",
        headers=HEADERS,
        json={"article": item["supplier_sku"]}
    )
```

### 5. Оценка эффективности
- Сложность: 3/5
- ROI: матчинг 500 позиций вручную — 4–6 ч; с Claude — 5 мин + 30 мин проверка спорных (~85% авто)

**Ссылки:** [[02_TOOLS/MoySklad_API]] | [[03_GUIDES/claude_api_batching]]
