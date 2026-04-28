---
source: YouTube / Bastian Hammer
date: 2026-03-23
original: https://youtube.com/watch?v=ahWJnhYT_ns
category: GOLD
tags: []
extracted_by: Claude Haiku
---

## Суть
Автоматизация синхронизации и создания контактов между Mautic (маркетинг-платформа) и SuiteCRM (CRM-система) через n8n (оркестратор воркфлоу). При добавлении или изменении контакта в Mautic он автоматически синхронизируется или создаётся в SuiteCRM, что обеспечивает единую базу данных и исключает ручную работу.

## Бизнес-сценарий
Маркетинг-компании, использующие Mautic для управления кампаниями и SuiteCRM для управления продажами, нуждаются в синхронизации контактов. n8n автоматизирует этот процесс: когда потенциальный клиент попадает в Mautic, он автоматически создаётся в SuiteCRM с правильной информацией (имя, email, телефон и т.д.), что ускоряет цикл продаж и снижает потери данных.

## Алгоритм реализации
1. Шаг 1: Настройка вебхука в Mautic. В администраторской панели Mautic (Settings → Webhooks) создать новый вебхук, который триггерится на событие 'Contact Created' или 'Contact Updated'. URL вебхука должен указывать на адрес n8n вебхука (например, https://your-n8n-instance.com/webhook/mautic-contact). Активировать событие и сохранить.
2. Шаг 2: Создание вебхука в n8n. Добавить ноду 'Webhook' (входящая точка). Выставить метод POST. Скопировать сгенерированный URL вебхука и вставить его в Mautic. Тестировать подключение, отправив тестовый контакт из Mautic.
3. Шаг 3: Извлечение данных контакта из вебхука. Добавить ноду 'Function' или 'Execute Script' для парсинга JSON-payload от Mautic. Извлечь поля: contact.id, contact.firstname, contact.lastname, contact.email, contact.phone, contact.mobile, contact.city, contact.state, contact.zip, contact.country и любые кастомные поля. Убедиться, что данные корректно мапируются.
4. Шаг 4: Проверка существования контакта в SuiteCRM. Добавить HTTP-запрос (HTTP Request ноду) к SuiteCRM API с эндпоинтом /module/Contacts, параметром filter по email. Это нужно для проверки, существует ли контакт уже в CRM. Использовать SuiteCRM REST API v10 или выше (oauth или API key auth).
5. Шаг 5: Условное создание/обновление контакта. Добавить If-ноду для ветвления логики: если контакт найден в SuiteCRM (по email) — выполнить UPDATE через PUT-запрос; если не найден — выполнить CREATE через POST-запрос. В обоих случаях использовать эндпоинт /module/Contacts. Передать все собранные поля из Mautic в body запроса.
6. Шаг 6: Обработка ошибок и логирование. Добавить ноду Error Handling для перехвата ошибок синхронизации (например, если контакт с таким email уже существует). Логировать успешные и неудачные синхронизации в Google Sheets или базе данных для аудита. Настроить алерты на email при критических ошибках.

## Технический стек
- n8n — оркестратор воркфлоу (no-code/low-code платформа для автоматизации)
- Mautic — маркетинг-автоматизационная платформа (источник контактов)
- SuiteCRM — open-source CRM-система (пункт назначения)
- Mautic Webhook — для отправки событий о контактах в n8n
- SuiteCRM REST API v10+ — для создания/обновления контактов
- OAuth 2.0 или API Key — аутентификация в SuiteCRM
- JSON — формат данных при передаче между системами
- HTTP Request (n8n ноды) — для запросов к SuiteCRM API
- Function/Script ноды (n8n) — для обработки и трансформации данных
- If/Condition ноды (n8n) — для условной логики

## Связки инструментов
- Webhook (Mautic) → n8n Webhook (триггер события о новом/изменённом контакте)
- n8n Function → парсинг и извлечение данных из Mautic payload
- n8n HTTP Request → SuiteCRM REST API /module/Contacts?filter (проверка наличия контакта)
- n8n If Condition → ветвление на CREATE (POST /module/Contacts) или UPDATE (PUT /module/Contacts/{id})
- SuiteCRM API Response → Google Sheets/Database (логирование результатов синхронизации)

## Конфигурация и параметры
- Mautic Webhook URL: Settings → Webhooks → Add Webhook → Event: 'Contact Created' или 'Contact Updated' → URL: https://your-n8n-instance.com/webhook/mautic-sync → Method: POST → активировать и сохранить
- Mautic API Payload структура: { contact: { id, firstname, lastname, email, phone, mobile, city, state, zip, country, [...customfields] } }
- SuiteCRM REST API эндпоинты: GET /module/Contacts?filter=(email eq '{email}') — поиск контакта; POST /module/Contacts — создание; PUT /module/Contacts/{id} — обновление
- SuiteCRM Authentication header: Authorization: Bearer {access_token} (для OAuth) или X-SUITECRM-API-KEY: {api_key} (для API Key)
- SuiteCRM Contacts module required fields: first_name, last_name, email1 (это обязательные поля в SuiteCRM, могут отличаться в зависимости от конфигурации)
- n8n Webhook ноды параметры: Метод: POST; Authentication: None (если не используется); Save Response: true
- n8n HTTP Request параметры к SuiteCRM: Method: GET (для проверки), POST (для создания), PUT (для обновления); Headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer {token}'} или X-SUITECRM-API-KEY; Params: filter=(email eq '{email}')
- Mapирование полей Mautic → SuiteCRM: mautic.firstname → first_name; mautic.lastname → last_name; mautic.email → email1; mautic.phone → phone_work или phone_mobile (в зависимости от конфигурации SuiteCRM)

## Ключевые инсайты
_Нет данных_

## Подводные камни
_Не упомянуты_
