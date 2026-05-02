---
title: Claude Opus 4.7 — автоматический разбор PDF-договоров и счетов в Bitrix24/МойСклад
tags: #biz_recipe #automation #bitrix24 #moysklad #opus47 #pdf #documents #action_needed
source: edvardgrishin27/169, rixaihub/442, ai_newz/4535
date: 2026-04-23
---

### 1. Описание идеи

Opus 4.7 значительно улучшил работу с документами: читает PDF до 40 страниц без ошибок, видит таблицы и реквизиты, следует инструкциям буквально. Практическое применение для CRM/ERP: менеджер загружает договор или счёт от поставщика → агент извлекает структурированные данные → автоматически создаёт сделку в Bitrix24 или контрагента в МойСклад. Ручной ввод исключается.

### 2. Технический стек

- AI: Claude Opus 4.7 (claude-opus-4-7) + Files API Anthropic
- CRM: Bitrix24 REST API (crm.deal.add, crm.company.add)
- ERP: МойСклад REST API (counterparty, invoicein)
- Middleware: n8n / Python-скрипт
- Источники PDF: email (Gmail/IMAP), Telegram-бот, папка на сервере

### 3. Пошаговый план внедрения

**Шаг 1 — Определить типы документов**
Выбрать 2–3 самых частых для автоматизации:
- Входящий счёт от поставщика → создать входящий счёт в МойСклад
- Договор с клиентом → создать сделку + компанию в Bitrix24
- Акт выполненных работ → закрыть задачу в Bitrix24

**Шаг 2 — Настройка источника PDF**
Вариант А (email): n8n Gmail Trigger → фильтр вложений по типу `application/pdf` → Base64
Вариант Б (Telegram): бот принимает файл → передаёт в n8n
Вариант В (папка): watchdog-скрипт на Python следит за `/inbox/` → при появлении файла запускает обработку

**Шаг 3 — Промпт для извлечения данных из договора**
```
Ты — ассистент по документообороту. Разбери документ и верни ТОЛЬКО JSON, без пояснений.

Из договора или счёта извлеки:
{
  "doc_type": "contract | invoice | act",
  "doc_number": "",
  "doc_date": "YYYY-MM-DD",
  "counterparty": {
    "name": "",
    "inn": "",
    "kpp": "",
    "address": "",
    "phone": "",
    "email": ""
  },
  "items": [
    {"name": "", "qty": 0, "unit": "", "price": 0, "amount": 0}
  ],
  "total_amount": 0,
  "currency": "RUB",
  "payment_due": "YYYY-MM-DD",
  "manager": "",
  "notes": ""
}

Если поле не найдено — верни null. Числа без пробелов и символов валюты.
```

**Шаг 4 — Загрузка PDF через Anthropic Files API**
```python
import anthropic, base64, json

client = anthropic.Anthropic()

def parse_pdf_document(pdf_path: str) -> dict:
    with open(pdf_path, "rb") as f:
        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data,
                    },
                },
                {
                    "type": "text",
                    "text": EXTRACTION_PROMPT  # промпт из шага 3
                }
            ],
        }],
    )

    raw = message.content[0].text.strip()
    # убрать возможный markdown-блок ```json ... ```
    if raw.startswith("```"):
        raw = raw.split("```")[1].lstrip("json").strip()
    return json.loads(raw)
```

**Шаг 5 — Создание записей в CRM/ERP**
```python
import requests

BITRIX_WEBHOOK = "https://your.bitrix24.ru/rest/1/TOKEN"

def create_deal_from_contract(data: dict):
    company_resp = requests.post(f"{BITRIX_WEBHOOK}/crm.company.add.json", json={
        "fields": {
            "TITLE":   data["counterparty"]["name"],
            "INN":     data["counterparty"]["inn"],
            "PHONE":   [{"VALUE": data["counterparty"]["phone"], "VALUE_TYPE": "WORK"}],
            "EMAIL":   [{"VALUE": data["counterparty"]["email"], "VALUE_TYPE": "WORK"}],
        }
    }).json()
    company_id = company_resp["result"]

    deal_resp = requests.post(f"{BITRIX_WEBHOOK}/crm.deal.add.json", json={
        "fields": {
            "TITLE":        f"Договор {data['doc_number']} от {data['doc_date']}",
            "COMPANY_ID":   company_id,
            "OPPORTUNITY":  data["total_amount"],
            "CURRENCY_ID":  data["currency"],
            "COMMENTS":     f"Срок оплаты: {data['payment_due']}\n{data['notes'] or ''}",
            "STAGE_ID":     "C1:NEW",
        }
    }).json()
    return deal_resp["result"]


def create_invoice_moysklad(data: dict):
    MS_TOKEN = "YOUR_MOYSKLAD_TOKEN"
    headers = {
        "Authorization": f"Bearer {MS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "name":         data["doc_number"],
        "moment":       f"{data['doc_date']}T00:00:00",
        "sum":          int(data["total_amount"] * 100),
        "agent": {
            "meta": {
                "href": f"https://api.moysklad.ru/api/remap/1.2/entity/counterparty/{data['counterparty']['inn']}",
                "type": "counterparty"
            }
        },
        "positions": [
            {
                "quantity": item["qty"],
                "price":    int(item["price"] * 100),
                "assortment": {"name": item["name"]}
            }
            for item in data["items"]
        ]
    }
    resp = requests.post(
        "https://api.moysklad.ru/api/remap/1.2/entity/invoicein",
        headers=headers, json=payload
    )
    return resp.json().get("id")
```

### 4. Нюансы Opus 4.7

- Новый токенизатор: PDF на 10 страниц раньше = ~8 000 токенов → теперь может быть до 10 800 (+35%). Учитывайте при расчёте стоимости
- Модель следует инструкциям буквально — если промпт требует чистый JSON, не добавит пояснений. Это плюс для парсинга
- Бенчи: Opus 4.7 справляется с ~90% задач там, где 4.6 справлялся с ~80% — для сложных договоров (нестандартная вёрстка, таблицы, сканы) результат заметно лучше
- Для сканированных PDF (не текстовый слой) добавить предобработку через Tesseract OCR перед отправкой в API

### 5. Оценка эффективности

- Сложность: 3/5
- ROI: ввод данных из одного договора вручную — 5–15 минут; агент делает это за 10–30 секунд; при 20 документах в день = 1,5–4 ч/день экономии; исключает ошибки ручного ввода ИНН, суммы, дат

**Ссылки:** [[02_TOOLS/Bitrix24_API]] | [[02_TOOLS/MoySklad_API]] | [[03_GUIDES/anthropic_files_api]]
