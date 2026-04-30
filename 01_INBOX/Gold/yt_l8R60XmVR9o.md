---
source: YouTube / Bastian Hammer
date: 2026-04-27
original: https://youtube.com/watch?v=l8R60XmVR9o
category: GOLD
tags: []
extracted_by: Claude Haiku
status: archive
reason: low_score
score: Pain=5 Dev=7 Profit=5 ИТОГ=17
---

## Суть
Автоматическая синхронизация контактов из Mautic в SuiteCRM через webhook и n8n. Когда в Mautic происходит событие (например, заполнение формы или изменение данных контакта), автоматически запускается процесс обновления или создания контакта в SuiteCRM без ручного вмешательства.

## Бизнес-сценарий
Растущие компании, которые используют Mautic для маркетинг-автоматизации и SuiteCRM как CRM, нуждаются в синхронизации данных контактов между системами. Workflow обрабатывает входящие webhook-события от Mautic и синхронизирует информацию о контактах (имя, email, номер телефона и т.д.) в SuiteCRM, обновляя существующих контактов или создавая новых.

## Алгоритм реализации
1. 1. Создание Webhook в n8n: Добавить ноду 'Webhook' в начало workflow'а. Установить метод HTTP на 'POST'. Скопировать URL webhook'а и добавить его в настройки Mautic (Admin → Webhooks → создать новый webhook с события 'Contact created' или 'Contact updated').
2. 2. Приём данных от Mautic: Webhook ноды получают JSON-payload с данными контакта (id, firstname, lastname, email, phone). Добавить ноду для парсинга данных или использовать автоматическое преобразование JSON.
3. 3. Проверка существования контакта в SuiteCRM: Добавить ноду 'HTTP Request' или встроенную ноду SuiteCRM для поиска контакта по email. Использовать фильтр: filter[email_addresses-email]={email} в API запросе к SuiteCRM.
4. 4. Условное ветвление (Switch/IF): Добавить ноду условия для проверки: если контакт найден → переходим к обновлению (UPDATE), если не найден → переходим к созданию (CREATE).
5. 5. Создание контакта в SuiteCRM: Для нового контакта использовать SuiteCRM API endpoint POST /Contacts с параметрами: first_name, last_name, email_addresses (массив с почтами), phone_numbers (массив с номерами). Настроить маппинг полей из Mautic в SuiteCRM.
6. 6. Обновление контакта в SuiteCRM: Для существующего контакта использовать endpoint PATCH /Contacts/{id} с теми же полями. n8n автоматически обновит только изменённые поля.
7. 7. Обработка ошибок и логирование: Добавить ноды для обработки ошибок (Error handling), логирования успешных операций и отправки уведомлений (опционально - email или Slack). Использовать ноды 'Set' для добавления временных меток и статусов.

## Технический стек
- n8n (workflow automation platform)
- Mautic (marketing automation CRM)
- SuiteCRM (open-source CRM)
- SuiteCRM REST API v10
- HTTP Request node (для API запросов)
- Webhook node (для получения событий)
- JSON parser/transformer nodes
- Switch/Conditional nodes (для логики ветвления)
- Set node (для маппинга данных)
- Error Handler node (для обработки ошибок)

## Связки инструментов
- Mautic Webhook Event → n8n Webhook Node (POST) → HTTP/SuiteCRM Node (Search Contact) → Switch (Condition) → Create Contact (POST /Contacts) ИЛИ Update Contact (PATCH /Contacts/{id}) → Success/Error Response

## Конфигурация и параметры
- Webhook Configuration: URL вида https://your-n8n-instance.com/webhook/mautic-crm-sync, HTTP Method: POST
- Mautic Admin Settings: Admin Panel → Webhooks → Add Event → выбрать 'contact.created' или 'contact.updated' → указать webhook URL n8n
- SuiteCRM API Credentials: API endpoint base URL (например https://your-suitecrm.com/api/v10), OAuth2 token или Basic Auth с username/password
- Mautic Payload Sample: {"id": 123, "firstname": "John", "lastname": "Doe", "email": "john@example.com", "phone": "+1234567890"}
- SuiteCRM API Search Endpoint: GET /Contacts?filter[email_addresses-email]={email}
- SuiteCRM Create Contact Endpoint: POST /Contacts с body: {"first_name": "John", "last_name": "Doe", "email_addresses": [{"email_address": "john@example.com", "primary_address": true}], "phone_numbers": [{"phone": "+1234567890"}]}
- SuiteCRM Update Contact Endpoint: PATCH /Contacts/{id} с аналогичным body структурой
- Field Mapping: Mautic firstname → SuiteCRM first_name, Mautic lastname → SuiteCRM last_name, Mautic email → SuiteCRM email_addresses[0].email_address, Mautic phone → SuiteCRM phone_numbers[0].phone

## Ключевые инсайты
- Webhook должен быть размещён на публичном URL без аутентификации (или с простой проверкой token'а) — Mautic должна иметь доступ к запуску.
- SuiteCRM использует REST API v10 с OAuth2 или Basic Auth — убедитесь, что у пользователя есть права на создание/редактирование контактов.
- Поиск контакта должен быть по email, так как это уникальный идентификатор — используйте фильтр filter[email_addresses-email]=email_value.
- Payload от Mautic может содержать дополнительные поля (custom fields) — убедитесь, что маппинг охватывает все необходимые поля.
- SuiteCRM требует структурированные массивы для email и phone — нельзя передать простую строку, нужен объект с подполями (email_address, phone и т.д.).
- Обработка ошибок критична — webhook должен возвращать статус 200 даже при ошибке (иначе Mautic будет повторять), логирование ошибок должно быть отделено от успеха.
- Тестирование webhook'а: используйте инструмент вроде Postman или встроенный тестер n8n для отправки mock-данных от Mautic перед подключением боевого окружения.

## Подводные камни
_Не упомянуты_
