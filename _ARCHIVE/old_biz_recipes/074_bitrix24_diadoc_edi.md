---
title: Bitrix24 + Диадок — двусторонний электронный документооборот
tags: #biz_recipe #bitrix24 #diadoc #edi #documents #automation #crm
source: yt_Fa-SfTUFm48
date: 2026-04-29
score: Pain=9 Dev=6 Profit=8 ИТОГ=23
---

### 1. Описание идеи

Компании выставляют счета в Bitrix24 и подписывают документы в Диадок (сервис ЭДО от Контур). Данные переносятся вручную в обе стороны. Двусторонняя интеграция: сделка «Оплачена» → автоматически создаётся пакет документов в Диадок. Контрагент подписал → статус в Bitrix24 обновляется.

### 2. Технический стек

- Bitrix24 REST API (Webhook `ONCRMDEALUPDATE`, `crm.deal.get`, `crm.contact.get`)
- Диадок API REST (https://diadoc.kontur.ru/api/)
- Авторизация Диадок: через OAuth2 или токен Диадок
- n8n / Python — оркестратор
- КЭП (квалифицированная электронная подпись) — для подписания документов

### 3. Пошаговый план внедрения

**Шаг 1 — Получить доступы**
```
Диадок API:
  diadoc.kontur.ru → Разработчикам → Получить Client ID и Client Secret
  POST /V3/Authenticate → получить AuthToken

Bitrix24:
  Администратор → Исходящие вебхуки → ONCRMDEALUPDATE
  → URL: n8n Webhook URL
```

**Шаг 2 — Создать документ в Диадок при закрытии сделки**
```javascript
// n8n: Bitrix24 Webhook → получить данные сделки
const deal = await bitrix24.deal.get(deal_id)
const contact = await bitrix24.contact.get(deal.CONTACT_ID)

// HTTP Request → Диадок API
POST https://diadoc-api.kontur.ru/V3/GenerateUniversalTransferDocumentXml
Headers:
  Authorization: DiadocAuth ddauth_api_client_id={{client_id}}, ddauth_token={{token}}
Body:
{
  "Seller": { "Inn": "{{myCompanyINN}}", "Name": "{{myCompanyName}}" },
  "Buyer":  { "Inn": "{{contact.INN}}", "Name": "{{contact.NAME}}" },
  "DocumentDate": "{{today}}",
  "DocumentNumber": "{{deal.ID}}",
  "Items": [{"Name": "{{deal.TITLE}}", "Price": {{deal.OPPORTUNITY}}, "Quantity": 1}]
}
```

**Шаг 3 — Отправить документ контрагенту**
```javascript
POST /V3/PostMessage
{
  "FromBoxId": "{{myBoxId}}",
  "ToBoxId": "{{counterpartyBoxId}}",  // BoxId контрагента в Диадок
  "DocumentAttachment": {
    "SignedContent": { "Content": "{{base64_xml}}", "Signature": "{{base64_signature}}" },
    "TypeNamedId": "UniversalTransferDocument"
  }
}
```

**Шаг 4 — Webhook от Диадок при подписании**
```
Диадок Events API → n8n Webhook:
  Событие: DocumentSigned (контрагент подписал)
  → HTTP Request → Bitrix24 crm.deal.update:
    STAGE_ID = "FINAL_INVOICE" (выставлен финальный счёт)
    UF_DIADOC_STATUS = "Подписан"
```

### 4. Сценарии использования

| Событие | Действие |
|---|---|
| Сделка «Выиграна» | Создать УПД в Диадок + отправить контрагенту |
| Контрагент подписал | Обновить статус в Bitrix24 |
| Контрагент отклонил | Задача менеджеру в Bitrix24 |
| Новый входящий документ | Создать контакт/сделку в Bitrix24 |

### 5. Нюансы

- BoxId контрагента в Диадок нужно получить заранее — не все компании в системе ЭДО
- КЭП нельзя хранить в облаке — подписание происходит на сервере с токеном (JaCarta, Рутокен)
- Диадок API имеет rate limit: 200 запросов/мин
- Для подключения КЭП к серверному подписанию нужна дополнительная настройка криптопровайдера

### 6. Оценка эффективности

- Сложность: 4/5 (КЭП + Диадок API специфичны)
- Время внедрения: 7–14 дней
- ROI: ручное создание пакета документов — 15–30 мин/сделку. При 20 сделках/день → 5–10 часов/день
