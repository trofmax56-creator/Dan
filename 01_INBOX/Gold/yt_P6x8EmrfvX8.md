---
source: YouTube / HeyReach
date: 2026-04-01
original: https://youtube.com/watch?v=P6x8EmrfvX8
category: GOLD
tags: []
extracted_by: Claude Haiku
status: ideas_lab
score: Pain=7 Dev=7 Profit=7 ИТОГ=21
---

## Суть
Автоматизация очистки и поддержки качества данных в HubSpot CRM с помощью n8n: удаление дублей контактов, валидация данных, обновление статусов и нормализация информации для поддержания чистоты базы данных без ручного вмешательства.

## Бизнес-сценарий
CRM-менеджеры, владельцы продаж и маркетеры используют этот workflow для автоматической очистки HubSpot от дублированных контактов, некорректных данных, устаревших записей и неправильно заполненных полей. Решает проблему деградации качества данных при масштабировании и интеграции с outbound-инструментами.

## Алгоритм реализации
1. Шаг 1: Создать trigger в n8n для мониторинга изменений в HubSpot (webhook или регулярное сканирование через Schedule node). Настроить эндпоинт для отслеживания создания/обновления контактов
2. Шаг 2: Подключить HubSpot API в n8n (интеграция с модулем HubSpot или HTTP-запросы). Указать API ключ и получить список контактов с критериями: пустые обязательные поля, дублирующиеся email/телефон
3. Шаг 3: Применить фильтры через Filter node для выявления некорректных записей: проверка валидности email (regex), наличие дублей по email/phone, проверка полей 'First Name', 'Last Name', 'Company'
4. Шаг 4: Для дублей — использовать HTTP-запрос к API HubSpot для получения списка контактов по критерию (email или phone), сравнить ID и создать условие для выбора мастер-контакта (старший по дате создания или по количеству взаимодействий)
5. Шаг 5: Выполнить merge дублей через HubSpot Merge Contacts API endpoint или удалить дубли через Delete Contact endpoint
6. Шаг 6: Обновить данные в HubSpot через Update Contact node: нормализовать форматы (UPPER/LOWER case для фамилий), заполнить пустые поля значениями по умолчанию, добавить теги для отслеженных контактов
7. Шаг 7: Создать логирование результатов (Google Sheets, Slack или встроенный логгер n8n) для отчётности: количество найденных дублей, обновлённых контактов, ошибок
8. Шаг 8: Настроить Schedule node для регулярного запуска workflow (еженедельно или ежедневно в ночное время). Добавить обработку ошибок и retry logic при сбое API

## Технический стек
- n8n (основная платформа автоматизации)
- HubSpot API (получение, обновление, удаление контактов)
- HTTP Request node (для кастомных запросов к HubSpot API)
- Filter node (фильтрация дублей и некорректных данных)
- Schedule node (регулярный запуск workflow)
- Google Sheets API (опционально, для логирования)
- Slack API (опционально, для уведомлений)
- Function node (для кастомной логики на JavaScript)
- Set node (для преобразования данных между шагами)

## Связки инструментов
- HubSpot API endpoint → n8n HTTP Request → Filter node → HubSpot Update/Delete endpoint
- Schedule trigger → HubSpot Get Contacts → Function (detect duplicates) → Merge/Update Contacts → Google Sheets (logging)
- Webhook (из HubSpot) → n8n workflow → Slack notification → Database log

## Конфигурация и параметры
- HubSpot API ключ: вставляется в Authentication поле HubSpot node или в HTTP header 'Authorization: Bearer YOUR_API_KEY'
- Эндпоинт для получения контактов: GET https://api.hubapi.com/crm/v3/objects/contacts?limit=100&archived=false
- Параметры фильтра: 'property' = 'email' или 'phone', условие поиска дублей через Search Contacts API с filterGroups
- Поле для сравнения дублей: 'hs_lead_status', 'createdate', 'hs_analytics_num_page_views'
- Merge API endpoint: POST https://api.hubapi.com/crm/v3/objects/contacts/merge (тело запроса содержит primaryObjectId и objectIdToMerge)
- Update Contact endpoint: PATCH https://api.hubapi.com/crm/v3/objects/contacts/{contactId} (в properties передаются обновляемые поля)
- Формат валидации email в Function node: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ (regex)
- Schedule frequency: '0 2 * * 0' (по cron) для запуска по воскресеньям в 2:00 AM
- Retry policy: максимум 3 попытки с интервалом 60 секунд при ошибках 429 (rate limit) и 5xx

## Ключевые инсайты
- HubSpot имеет встроенный API для merge контактов, но merge можно выполнить только если контакты имеют одинаковый email или phone — это критическое условие при выборе мастер-контакта
- Rate limit в HubSpot API: 100 запросов в 10 секунд на бесплатном плане. Используйте batch-операции (Search API с limit=100) вместо множественных GET запросов для каждого контакта
- Обязательно проверьте поле 'archived' при выборке контактов (добавьте &archived=false), иначе будете обновлять удалённые контакты
- Дубли часто образуются при интеграции с outbound-инструментами (LinkedIn Sales Navigator, Apollo, Hunter). Лучше предотвратить дубли на входе (проверка перед созданием) чем удалять их потом
- При нормализации данных (UPPER/LOWER case) проверьте, что это не нарушает исторические данные и отчёты, привязанные к этим полям
- Используйте теги (tags) в HubSpot для отслеживания контактов, прошедших через автоматизацию: 'hygiene_processed_[date]' — это упростит отчётность и повторную обработку
- Функция JSON парсинга при работе с вложенными объектами HubSpot (associations, custom properties) требует использования Function node или формул в Set node
- Важно различать типы дублей: soft duplicates (неполные данные) требуют merge, hard duplicates (полностью идентичные email+name) требуют удаления мастера с менее значимыми данными

## Подводные камни
_Не упомянуты_
