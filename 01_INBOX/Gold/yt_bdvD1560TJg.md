---
source: YouTube / Business Workflow
date: 2026-04-16
original: https://youtube.com/watch?v=bdvD1560TJg
category: GOLD
tags: []
extracted_by: Claude Haiku
---

## Суть
Автоматизация процесса синхронизации контактов из SmartLead в Attio CRM с анализом статуса "Do not contact" через платформу Make.com, чтобы оптимизировать рабочий процесс продаж и исключить недействительные контакты из воронки.

## Бизнес-сценарий
Продажные команды и Sales Development Representatives (SDR) используют эту автоматизацию для синхронизации потенциальных клиентов из SmartLead (платформы поиска контактов) в Attio CRM. Система анализирует статус контактов, отфильтровывает записи с меткой "Do not contact" и создает или обновляет записи только валидных контактов в CRM, экономя время на ручной обработке данных.

## Алгоритм реализации
1. Шаг 1: Триггер вебхука — получение события из SmartLead (новые контакты, обновления статусов) через вебхук-URL в Make.com
2. Шаг 2: Парсинг входящих данных — извлечение полей контакта: email, имя, фамилия, компания, статус 'Do not contact' и другие параметры
3. Шаг 3: Условное разветвление (Router/Filter) — проверка статуса 'Do not contact': если true, то поток прерывается; если false, переход к следующему шагу
4. Шаг 4: Проверка существования контакта в Attio — поиск контакта по email в CRM через API запрос (GET endpoint)
5. Шаг 5: Логика создания или обновления — если контакт существует, выполняется UPDATE (PATCH/PUT запрос с новыми данными), если нет — CREATE (POST запрос с полным объектом контакта)
6. Шаг 6: Маппирование полей SmartLead → Attio — преобразование структуры данных из формата SmartLead в формат Attio CRM с соответствием названий полей
7. Шаг 7: Отправка данных в Attio API — POST/PATCH запрос с авторизацией (API ключ/токен Attio в заголовках)
8. Шаг 8: Логирование результата — сохранение ID созданного/обновленного контакта, статуса операции и ошибок в логе для аудита

## Технический стек
- Make.com (платформа автоматизации)
- SmartLead API (извлечение контактов)
- Attio CRM API (запись контактов)
- Webhooks (трансферт данных в реальном времени)
- JSON (формат данных)
- REST API (HTTP методы: GET, POST, PATCH, PUT)
- API аутентификация (Bearer token, API ключи)
- Условная логика (if/else, routing)
- Функции трансформации данных (map/filter)

## Связки инструментов
- Webhook (SmartLead события) → Make.com Webhook модуль → Router (условие: Do not contact?) → Attio API (Create/Update контакт) → Логирование результата
- SmartLead API → JSON парсер → Field Mapper → Attio CRM Database
- Real-time sync: SmartLead trigger → Make.com automation → Attio API endpoint

## Конфигурация и параметры
- Webhook URL в Make.com: скопировать уникальный URL и добавить его в SmartLead интеграцию
- Аутентификация SmartLead: использование API ключа SmartLead в заголовках запроса (Authorization: Bearer YOUR_SMARTLEAD_API_KEY)
- Аутентификация Attio: использование API ключа/токена Attio (Authorization: Bearer YOUR_ATTIO_API_KEY)
- Поле 'Do not contact': название поля в SmartLead (возможные варианты: 'dnc', 'do_not_contact', 'unsubscribe_status')
- Attio API endpoint для создания контакта: POST /contacts или /crm/contacts
- Attio API endpoint для поиска контакта: GET /contacts?email={{email}} или GET /contacts/search
- Attio API endpoint для обновления контакта: PATCH /contacts/{{contact_id}}
- Маппирование полей: SmartLead.email → Attio.email, SmartLead.first_name → Attio.first_name, SmartLead.last_name → Attio.last_name, SmartLead.company → Attio.company
- Условие фильтра: if (SmartLead.do_not_contact == true || SmartLead.do_not_contact == 'yes') then STOP else CONTINUE
- Обработка ошибок: настройка error handling для обработки случаев, когда Attio API возвращает 400/409 (конфликт, дублинг)

## Ключевые инсайты
- SmartLead интегрируется по вебхукам, что позволяет синхронизировать контакты в режиме реального времени, а не батчами
- Критический фильтр 'Do not contact' предотвращает попадание нежелательных контактов в CRM и убережет компанию от спама-жалоб
- Проверка существования контакта перед созданием (deduplicate) экономит API-квоты Attio и избегает дублирования записей
- При обновлении контакта используется PATCH вместо PUT, чтобы обновлять только измененные поля, не перезаписывая все значения
- API ключи SmartLead и Attio должны храниться в защищенном хранилище Make.com (переменные окружения), а не в открытом тексте
- Маппирование полей должно быть двусторонним: проверьте документацию обеих платформ для совпадения названий полей (snake_case vs camelCase)
- Отправка пользовательских полей (custom fields) из SmartLead требует предварительного создания этих полей в Attio и указания их ID
- Рекомендуется добавить логирование и webhook на ошибки для мониторинга: если синхронизация упала, отправить алерт в Slack или email

## Подводные камни
_Не упомянуты_
