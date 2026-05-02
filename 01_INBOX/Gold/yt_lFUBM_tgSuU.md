---
source: YouTube / Learn It Fast
date: 2026-04-04
original: https://youtube.com/watch?v=lFUBM_tgSuU
category: GOLD_CRM
tags: []
extracted_by: Claude Haiku
---

## Суть
Подключение Facebook Lead Ads к n8n для автоматизации сбора и обработки данных потенциальных клиентов. Данное решение позволяет автоматически захватывать лиды из Facebook, передавать их в n8n и интегрировать с CRM или другими системами, исключая ручную работу с данными.

## Бизнес-сценарий
Маркетолог или владелец бизнеса использует Facebook Lead Ads для сбора контактных данных потенциальных клиентов. Система автоматически перенаправляет полученные лиды в n8n для обработки, валидации и синхронизации с amoCRM, Bitrix24 или другим CRM, избегая потери данных и ускоряя работу отделов продаж.

## Алгоритм реализации
1. Шаг 1: Создать приложение Facebook и получить доступ к Lead Ads API. В Facebook Developer Console перейти в Apps, создать новое приложение или использовать существующее, добавить тип приложения 'Business'. Получить Access Token из раздела Settings > Basic, скопировать App ID и App Secret.
2. Шаг 2: В n8n создать новый workflow. Добавить триггер 'Webhook' для получения данных от Facebook (используется Webhook URL из n8n). Или использовать 'HTTP Request' ноду для периодического опроса Facebook API.
3. Шаг 3: Настроить подписку на события Lead Ads в Facebook. В Facebook App Settings перейти в Webhooks, указать Webhook URL из n8n, выбрать события 'leadgen.data_created' для автоматического получения лидов.
4. Шаг 4: В n8n добавить ноду 'HTTP Request' для парсинга входящих данных от Facebook. Указать параметры: Method - POST, URL - endpoint Facebook API (graph.facebook.com/v19.0/me/leadgen_forms), Headers - Authorization с Bearer токеном.
5. Шаг 5: Добавить ноду для трансформации данных (Extract/Transform Data). Извлечь нужные поля: email, phone, name, company из payload Facebook. Использовать ноду 'Item Lists' или 'Function' для структурирования.
6. Шаг 6: Добавить ноду 'Condition' для валидации данных. Проверить наличие обязательных полей (email или phone). Если данные неполные, отправить в отдельный поток обработки ошибок.
7. Шаг 7: Интегрировать с целевой CRM (amoCRM, Bitrix24 или Google Sheets). Добавить ноду 'amoCRM' или 'HTTP Request' с настройкой эндпоинта создания контакта. Передать структурированные данные лида: POST /api/v4/contacts с заголовками Authorization и Content-Type: application/json.
8. Шаг 8: Добавить ноду логирования (Logger) или отправки уведомлений. Настроить отправку Slack-сообщения или email при успешном добавлении лида. Указать канал: #sales или email: sales@company.com.

## Технический стек
- n8n (workflow automation platform)
- Facebook Lead Ads API
- Facebook Graph API (v19.0 или выше)
- Webhook (для получения real-time событий от Facebook)
- HTTP Request (для API вызовов)
- Facebook Developer Console
- amoCRM API (или альтернатива: Bitrix24 API, Google Sheets API)
- Access Token (OAuth 2.0)
- JSON (формат данных)
- Slack API (опционально для уведомлений)
- Logger/Debug ноды для отладки

## Связки инструментов
- Facebook Lead Ads Event → Webhook → n8n → HTTP Request (парсинг) → Condition (валидация) → amoCRM API (создание контакта)
- Альтернативный поток: Facebook Graph API (опрос) → n8n HTTP Request → Transform Data → Bitrix24 REST API → Slack Notification

## Конфигурация и параметры
- Facebook App Settings: Webhook URL - скопировать из n8n Webhook ноды (формат: https://your-n8n-instance.com/webhook/your-webhook-path)
- Webhook Events: выбрать 'leadgen.data_created' и 'leadgen_form' события
- Access Token: получить из Facebook App Dashboard, Settings > Basic, скопировать ключ 'App Access Token' или 'User Access Token'
- n8n Webhook ноды параметры: Method - POST, Authentication - None (если Open), Query Parameters - 'challenge' параметр для Facebook verification
- HTTP Request нода для Facebook API: URL параметр - https://graph.facebook.com/v19.0/{leadgen_form_id}/leads?access_token={ACCESS_TOKEN}
- Поля лида из Facebook payload: 'id' (ID лида), 'created_time' (время создания), 'field_data' (массив с полями: {name, phone_number, email, company, etc})
- CRM интеграция (amoCRM пример): эндпоинт POST /api/v4/contacts, headers {'Authorization': 'Bearer {API_KEY}', 'Content-Type': 'application/json'}, body содержит {name, phone, email, status_id}
- Data Transform: использовать map() функцию для преобразования field_data массива в объект {email: ..., phone: ..., name: ..., company: ...}

## Ключевые инсайты
_Нет данных_

## Подводные камни
_Не упомянуты_
