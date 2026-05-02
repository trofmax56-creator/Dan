---
source: YouTube / Bastian Hammer
date: 2026-04-27
original: https://youtube.com/watch?v=8wBwhvi2X_Q
category: GOLD_CRM
tags: []
extracted_by: Claude Haiku
---

## Суть
Интеграция Mautic, SuiteCRM и n8n для автоматического обновления и синхронизации контактов: при срабатывании webhook-события в Mautic контакты автоматически отправляются в SuiteCRM через n8n, что обеспечивает двусторонний обмен данными между маркетинг-платформой и CRM.

## Бизнес-сценарий
Растущие компании, использующие Mautic для маркетинг-автоматизации и SuiteCRM для управления контактами, синхронизируют данные контактов при изменении их статуса в Mautic (например, добавление в лист, изменение поля) напрямую в SuiteCRM через n8n workflow, избегая ручных обновлений и дублирования данных.

## Алгоритм реализации
1. Шаг 1: Создание Webhook в Mautic — перейти в Mautic → Settings → Webhooks → Create New. Выбрать событие (например 'Contact Timeline', 'Form submission' или другое). Скопировать webhook URL для использования в n8n.
2. Шаг 2: Создание workflow в n8n — создать новый workflow, добавить триггер 'Webhook' с типом 'Listen to POST requests'.
3. Шаг 3: Настройка Mautic Webhook ноды в n8n — добавить ноду 'Webhook' с методом POST, указать URL из Mautic webhook и настроить условия срабатывания (например, при добавлении контакта или обновлении поля).
4. Шаг 4: Обработка данных контакта — добавить ноды для парсинга JSON-ответа из Mautic (используя Function или Script ноды для трансформации данных), извлечение полей: email, firstname, lastname, phone, custom_fields и пр.
5. Шаг 5: Создание/Обновление контакта в SuiteCRM — добавить ноду SuiteCRM (или HTTP Request с API SuiteCRM), метод POST/PUT для создания или обновления контакта. Указать URL эндпоинта SuiteCRM API (например /rest/v11/Contacts), передать поля: first_name, last_name, email, phone и прочие необходимые параметры из Mautic.
6. Шаг 6: Обработка ошибок и логирование — добавить условные блоки (If/Else) для проверки статуса ответа от SuiteCRM (200, 201, 400 и т.д.), при ошибке отправить уведомление или записать в лог.
7. Шаг 7: Активация workflow — опубликовать workflow и указать его webhook URL в Mautic для автоматического срабатывания при событиях контакта.

## Технический стек
- n8n (workflow automation platform)
- Mautic (marketing automation, webhook events)
- SuiteCRM (CRM system, REST API v11)
- HTTP Request (для API SuiteCRM)
- Webhook trigger (для входящих POST-запросов от Mautic)
- Function/Script ноды (для парсинга и трансформации данных)
- JSON (формат передачи данных)
- REST API (SuiteCRM API для CRUD операций с контактами)

## Связки инструментов
- Mautic Webhook → n8n Webhook trigger → Function node (парсинг контакта) → SuiteCRM API (HTTP Request node) → Проверка статуса и логирование

## Конфигурация и параметры
- Mautic webhook URL: должен содержать базовый URL Mautic, например https://your-mautic-domain.com
- n8n Webhook: POST endpoint, например https://your-n8n-domain.com/webhook/mautic-contact-sync
- SuiteCRM API эндпоинт: /rest/v11/Contacts (для создания) или /rest/v11/Contacts/{id} (для обновления)
- Параметры парсинга контакта из Mautic: event (тип события), contact.id, contact.email, contact.firstname, contact.lastname, contact.phone, contact.custom_fields
- Поля SuiteCRM API: first_name, last_name, email, phone, description, assigned_user_id, team_id, account_name и др.
- Аутентификация SuiteCRM: OAuth2 или API токен, передавать в заголовке Authorization: Bearer {token}
- Метод запроса к SuiteCRM: POST для создания (запрос без id), PUT для обновления (с id в URL или теле запроса)

## Ключевые инсайты
- Webhook в Mautic срабатывает при определённых событиях (добавление контакта, изменение поля, добавление в лист), автоматически отправляя POST-запрос с данными контакта на URL n8n
- n8n Webhook node слушает входящие запросы и инициирует workflow без необходимости полинга API Mautic
- Парсинг JSON-ответа Mautic критичен: структура данных может быть вложенной (contact object содержит nested fields), используй Function ноду для извлечения нужных полей
- SuiteCRM API требует правильного формата полей (snake_case для API): firstname в Mautic становится first_name в SuiteCRM
- Для обновления существующего контакта в SuiteCRM нужно проверить, есть ли уже контакт с таким email: либо хранить Mautic ID в SuiteCRM, либо использовать filter по email при поиске
- Ошибки интеграции часто возникают из-за несовпадения формата полей, отсутствия Required fields или неправильной аутентификации к SuiteCRM API
- Используй Error Handling (Try/Catch или условные блоки If-Else) для обработки ошибок API SuiteCRM и отправки уведомлений при сбое синхронизации
- Логирование всех синхронизаций в базу данных или файл помогает отладить проблемы с конкретными контактами

## Подводные камни
_Не упомянуты_
