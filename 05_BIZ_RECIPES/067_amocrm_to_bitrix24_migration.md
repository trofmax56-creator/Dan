---
title: Миграция AmoCRM → Bitrix24 — алгоритм переноса без потерь
tags: #biz_recipe #amocrm #bitrix24 #migration #crm #consulting
source: yt_0IJT0LtcniQ
date: 2026-04-29
score: Pain=9 Dev=6 Profit=9 ИТОГ=24
---

### 1. Описание идеи

Клиент платит за AmoCRM + отдельно за каждую интеграцию (телефония, мессенджеры, email-трекинг, аналитика). Сумма нередко превышает ₽30–50k/мес. Bitrix24 содержит большинство этих функций «из коробки». Услуга: аудит текущих интеграций AmoCRM → расчёт экономии → миграция данных → настройка Bitrix24.

Средний чек проекта: ₽60 000–150 000. ROI для клиента — окупаемость за 2–3 месяца.

### 2. Технический стек

- AmoCRM API v4 (`/api/v4/leads`, `/api/v4/contacts`, `/api/v4/companies`)
- Bitrix24 REST API (`crm.deal.import`, `crm.contact.add`, `crm.company.add`)
- Python 3 / n8n — для скрипта миграции
- Google Sheets — промежуточное хранилище для маппинга полей
- Postman / curl — тестирование API

### 3. Пошаговый план внедрения

**Шаг 1 — Аудит AmoCRM**
```
Составить список:
✓ Все активные интеграции + их стоимость
✓ Кастомные поля в сделках и контактах
✓ Воронки продаж (этапы, статусы)
✓ Автоматизации (триггеры, боты AmoCRM)
✓ Количество сделок / контактов / компаний
```

**Шаг 2 — Экспорт данных из AmoCRM**
```python
import requests

headers = {"Authorization": f"Bearer {AMOCRM_TOKEN}"}
base = "https://your-domain.amocrm.ru/api/v4"

# Экспорт контактов
contacts = []
page = 1
while True:
    r = requests.get(f"{base}/contacts?page={page}&limit=250", headers=headers)
    data = r.json().get("_embedded", {}).get("contacts", [])
    if not data: break
    contacts.extend(data)
    page += 1

# Аналогично для leads, companies
```

**Шаг 3 — Маппинг полей (Google Sheets)**
```
AmoCRM поле          → Bitrix24 поле
contact.name         → NAME
contact.first_name   → NAME (часть)
contact.custom_fields[phone] → PHONE
lead.price           → OPPORTUNITY
lead.pipeline_id     → STAGE_ID (перекодировать)
lead.status_id       → STAGE_ID
```

**Шаг 4 — Импорт в Bitrix24**
```python
b24_url = "https://your-domain.bitrix24.ru/rest/1/YOUR_TOKEN"

for contact in contacts:
    payload = {
        "fields": {
            "NAME": contact["name"],
            "PHONE": [{"VALUE": p["value"], "VALUE_TYPE": "WORK"}
                      for p in contact.get("custom_fields_values", [])
                      if p["field_code"] == "PHONE"],
            "EMAIL": [{"VALUE": e["value"], "VALUE_TYPE": "WORK"}
                      for e in contact.get("custom_fields_values", [])
                      if e["field_code"] == "EMAIL"],
        }
    }
    requests.post(f"{b24_url}/crm.contact.add.json", json=payload)
```

**Шаг 5 — Настройка воронок и автоматизаций в Bitrix24**
- Создать воронки с теми же этапами, что были в AmoCRM
- Настроить роботов Bitrix24 вместо ботов AmoCRM
- Подключить встроенную телефонию (Bitrix24 Телефония — бесплатно)
- Настроить открытые линии для Telegram/WhatsApp

### 4. Сценарии использования

| Что переносим | Метод | Сложность |
|---|---|---|
| Контакты + компании | API batch import | Низкая |
| Сделки с историей | API + маппинг этапов | Средняя |
| Файлы и вложения | Скачать → загрузить в Диск Bitrix24 | Высокая |
| Автоматизации | Пересоздать вручную | Средняя |
| Интеграции | Битрикс24 встроенные | Низкая |

### 5. Нюансы

- История переписки (звонки, письма) переносится частично — зависит от AmoCRM тарифа и наличия API
- Кастомные поля нужно создать в Bitrix24 до импорта, иначе данные потеряются
- Воронки в Bitrix24 строже по структуре: нельзя иметь сделку «без этапа»
- Рекомендовать клиенту Bitrix24 Cloud (а не коробку) — проще поддерживать

### 6. Оценка эффективности

- Сложность: 3/5
- Время внедрения: 5–14 дней (зависит от объёма данных)
- ROI для клиента: экономия ₽15–40k/мес на интеграциях уже с первого месяца
- Маржа исполнителя: ₽40–80k за проект при себестоимости 3–5 рабочих дней
