---
title: Bitrix24 + n8n + WhatsApp — ИИ-ответ на пропущенный звонок через Voximplant
tags: #biz_recipe #automation #bitrix24 #n8n #whatsapp #action_needed
---

### 1. Описание идеи
Когда менеджер пропустил звонок, "горячий" лид остывает за 5–15 минут. Вебхук `OnVoximplantCallMissed` в Bitrix24 запускает n8n: Claude формирует персонализированное сообщение (имя из CRM + контекст сделки) и отправляет его клиенту в WhatsApp через API. Лид удерживается без участия менеджера.

### 2. Технический стек
- AI: Claude API (claude-sonnet-4-6)
- CRM/ERP: Bitrix24 (облако, с Voximplant)
- Middleware: n8n (self-hosted), WhatsApp Business API (или waba.io / green-api.com)

### 3. Пошаговый план внедрения
1. В Bitrix24 → Настройки → Исходящие вебхуки: добавить событие `OnVoximplantCallMissed`, URL = n8n webhook
2. В n8n — Webhook-триггер: получить `PHONE_NUMBER`, `CALLER_ID`, `RESPONSIBLE_ID`
3. HTTP Request → `crm.contact.list` (фильтр по телефону) — получить имя контакта и `DEAL_ID`
4. HTTP Request → `crm.deal.get` — получить стадию сделки и сумму
5. Claude API node: сгенерировать сообщение (промпт ниже)
6. HTTP Request → WhatsApp API: отправить сообщение на `PHONE_NUMBER`
7. HTTP Request → `crm.activity.add` в Bitrix24 — зафиксировать отправку как активность

### 4. Промпты и Код
```
SYSTEM:
Ты — вежливый менеджер по продажам. Напиши короткое WhatsApp-сообщение (2–3 предложения)
клиенту, которому не смогли ответить на звонок. Тон: дружелюбный, без извинений "простите".
Предложи перезвонить или написать удобное время. Не упоминай компанию в конце.

USER:
Имя клиента: {contact_name}
Стадия сделки: {deal_stage}
Сумма сделки: {deal_sum} руб.
```

```json
// n8n HTTP Request — отправка через green-api.com
{
  "method": "POST",
  "url": "https://api.green-api.com/waInstance{{$env.WABA_INSTANCE}}/sendMessage/{{$env.WABA_TOKEN}}",
  "body": {
    "chatId": "7{{ $json.phone_clean }}@c.us",
    "message": "{{ $json.claude_response }}"
  }
}
```

```js
// n8n Function node — нормализация номера телефона
const raw = $input.first().json.PHONE_NUMBER || "";
const clean = raw.replace(/\D/g, "").replace(/^8/, "7");
return [{ json: { phone_clean: clean } }];
```

```json
// Bitrix24 — фиксация активности после отправки
// POST crm.activity.add
{
  "fields": {
    "OWNER_TYPE_ID": 2,
    "OWNER_ID": "{{ deal_id }}",
    "TYPE_ID": 4,
    "SUBJECT": "WhatsApp: ответ на пропущенный звонок (авто)",
    "DESCRIPTION": "{{ claude_response }}",
    "COMPLETED": "Y",
    "DIRECTION": 2
  }
}
```

### 5. Оценка эффективности
- Сложность: 3/5
- ROI: удержание до 30% "пропущенных" лидов; реакция < 1 мин вместо 15–60 мин ручного перезвона

**Ссылки:** [[02_TOOLS/n8n_setup]] | [[03_GUIDES/bitrix24_webhooks]] | [[03_GUIDES/whatsapp_api]]
