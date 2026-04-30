---
source: YouTube / AI Mastery
date: 2026-04-17
original: https://youtube.com/watch?v=7sB4OO4XM0w
category: GOLD
tags: []
extracted_by: Claude Haiku
status: ideas_lab
score: Pain=6 Dev=8 Profit=5 ИТОГ=19
---

## Суть
Автоматизация создания встреч Zoom через n8n для программного развёртывания надёжных видеоконференций. Позволяет автоматически генерировать ссылки на встречи и управлять ними без ручного участия.

## Бизнес-сценарий
SaaS-платформы, онлайн-образование, служба поддержки клиентов используют автоматическое создание встреч Zoom при регистрации пользователей, бронировании консультаций или запросе демо-звонка. Обрабатывает данные о пользователе (имя, email, время) и автоматически создаёт встречу с нужными параметрами.

## Алгоритм реализации
1. 1. Установка и подключение Zoom API в n8n: добавляем узел 'Zoom' и авторизуемся через OAuth 2.0, получив credentials с Zoom App Marketplace
2. 2. Создание триггера для начала workflow: выбираем webhook, форму или другой источник данных (например, ввод email и названия встречи)
3. 3. Настройка узла 'Zoom Create Meeting': заполняем обязательные поля - topic (название встречи), start_time (время начала в формате ISO 8601), duration (длительность в минутах), type (1 = одноразовая встреча)
4. 4. Конфигурирование параметров встречи: включаем опции host video, participant video, join before host, mute upon entry, waiting room, recording settings в зависимости от требований
5. 5. Обработка ответа от Zoom API: извлекаем join_url (ссылка для участников) и host_url (ссылка для организатора) из возвращённых данных
6. 6. Сохранение данных: отправляем полученные URLs и детали встречи в CRM/БД (Airtable, Google Sheets, Bitrix24) для последующего использования
7. 7. Отправка уведомления: используем email node для отправки приглашения с ссылкой на встречу участникам
8. 8. Добавление обработки ошибок: настраиваем условные блоки (if-then) для обработки случаев, когда Zoom API вернул ошибку (например, неверное время)

## Технический стек
- n8n (workflow automation platform)
- Zoom API v2 (https://zoom.us/developers/)
- Zoom App Marketplace (для регистрации приложения и получения Client ID, Client Secret)
- HTTP Request node (для кастомных API запросов)
- Email node (для отправки приглашений)
- Webhook trigger (для запуска workflow)
- Database nodes (Google Sheets, Airtable, PostgreSQL для хранения данных)
- Bitrix24 API (опционально для интеграции с CRM)
- JSON processing (для парсинга ответов API)

## Связки инструментов
- Webhook (входящий) → n8n Zoom Node → Zoom API v2 Create Meeting endpoint
- Zoom API Response (join_url, host_url, meeting_id) → Google Sheets/Airtable (сохранение)
- n8n Email Node → SMTP сервер → Email участнику с ссылкой
- Error Handler → Slack/Email notification о ошибке при создании встречи

## Конфигурация и параметры
- Zoom API Endpoint: POST /v2/users/{userId}/meetings
- Обязательные поля в теле запроса: topic (string), type (integer: 1 для одноразовой встречи), start_time (ISO 8601 формат, например '2026-01-15T10:00:00Z'), duration (integer минут)
- Опциональные параметры: agenda (description), host_video (boolean), participant_video (boolean), join_before_host (boolean), mute_upon_entry (boolean), waiting_room (boolean), auto_recording ('record_locally' или 'record_cloud' или 'none')
- Аутентификация: OAuth 2.0 с использованием Access Token (не API Key, которые deprecated)
- n8n Zoom Node полях: Meeting Topic, Meeting Type, Start Time (выбор даты/времени), Duration, Meeting Settings (чекбоксы для video, waiting room и т.д.)
- Возвращаемые значения: id (meeting_id), join_url (ссылка для гостей), host_url (ссылка для организатора), start_url (альтернатива host_url), password (если требуется для присоединения)
- Timezone: при установке start_time указывается timezone_id (например 'America/Los_Angeles' или 'Europe/Moscow')
- User ID: указывается либо 'me' (текущий авторизованный пользователь) либо конкретный Zoom user ID

## Ключевые инсайты
- Используйте OAuth 2.0 вместо устаревших API ключей — это обязательно для современной Zoom API v2
- Время встречи всегда передавайте в UTC или с явным указанием timezone_id, иначе встреча может создаться в неправильное время
- Максимальное количество встреч, которые можно создать программно — зависит от плана подписки Zoom (обычно не лимитировано, но есть rate limits: 300 запросов в минуту на приложение)
- join_url vs host_url: участники используют join_url, а организатор может использовать как join_url так и host_url (host_url автоматически запускает клиент Zoom)
- Waiting room — мощный инструмент для контроля, кто входит на встречу; можно включить в настройках по умолчанию для всех встреч
- Recording: если включить auto_recording: 'record_cloud', все встречи автоматически записываются в облако Zoom (требует облачного хранилища)
- Webhook триггер n8n должен быть настроен на listen для POST запросов, иначе workflow не запустится автоматически
- Обрабатывайте случаи, когда пользователь вводит время в прошлом — Zoom API вернёт ошибку 300; добавьте валидацию с помощью JavaScript функций n8n
- Ограничение Zoom: встреча может быть создана максимум на 6 месяцев вперёд (проверяйте дату перед запросом)

## Подводные камни
_Не упомянуты_
