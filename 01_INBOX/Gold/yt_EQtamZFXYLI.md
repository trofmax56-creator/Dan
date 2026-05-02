---
source: YouTube / Hartwell Explain
date: 2026-04-30
original: https://youtube.com/watch?v=EQtamZFXYLI
category: GOLD
tags: []
extracted_by: Claude Haiku
---

## Суть
Подключение и интеграция Pipedrive с Make.com для автоматизации рабочих процессов управления продажами. Автоматизация позволяет исключить ручные, повторяющиеся задачи и синхронизировать данные между платформами в реальном времени.

## Бизнес-сценарий
Sales teams, CRM managers и small/mid-size businesses используют Pipedrive для управления продажами и Make.com для создания автоматизированных workflows. Типичные сценарии: синхронизация новых контактов, автоматическое создание сделок, уведомления о статусе, экспорт данных в другие системы.

## Алгоритм реализации
1. Шаг 1: Создание аккаунта на Make.com (если его нет) и авторизация в Pipedrive через API-ключ. Перейдите в Pipedrive Settings → Personal Preferences → API, скопируйте API Token.
2. Шаг 2: В Make.com нажмите 'Create a new scenario' и выберите trigger 'Pipedrive' → выберите нужное событие (например, 'Watch Deals' для отслеживания новых сделок).
3. Шаг 3: Установите соединение с Pipedrive: нажмите 'Add' в поле Connection, вставьте скопированный API Token, выберите компанию/рабочее пространство.
4. Шаг 4: Настройте параметры trigger (например, фильтры по статусу сделки, стадии воронки, владельцу). Выберите какие поля отслеживать (deal amount, stage, owner_id и т.д.).
5. Шаг 5: Добавьте action-ноду (например, 'Send an email', 'Create a record in Google Sheets', 'Send Slack notification'). Настройте маппинг полей из Pipedrive в целевую систему.
6. Шаг 6: Тестирование workflow: нажмите 'Run once', проверьте логи, убедитесь что данные маппятся корректно, нет ошибок аутентификации.
7. Шаг 7: Активируйте сценарий (toggle 'ON'), настройте schedule (Immediate execution или by schedule). Мониторьте выполнение в разделе 'Execution history'.

## Технический стек
- Make.com (formerly Integromat) — платформа для automation workflows
- Pipedrive API v1 и v2 — REST API для управления контактами, сделками, этапами
- API Token/API Key — аутентификация в Pipedrive
- Webhook (опционально) — для real-time триггеров
- JSON data format — обмен данными между системами
- HTTP Request модуль (для custom API calls)
- Встроенные Make.com коннекторы для Google Sheets, Slack, Email, Zapier и других сервисов

## Связки инструментов
- Webhook (входящий запрос) → Make.com Pipedrive Trigger (Watch Deals/Contacts) → Фильтр данных → Action (Email/Slack/Database)
- Pipedrive API Token → Make.com Connection Settings → Authenticated API requests
- Make.com Scenario → Test Run → Execution Logs → Live Monitoring Dashboard

## Конфигурация и параметры
- Pipedrive Settings: Personal Preferences → API section, копирование API Token (38-символьная строка)
- Make.com Connection: тип 'Pipedrive' → поле 'API Key' → выбор базовой компании (company root ID)
- Trigger Module Settings: Watch Deals — параметры 'Stage ID' (опционально для фильтра), 'Include Custom Fields' (yes/no), 'Limit' (количество результатов)
- Action Module (пример Send Email): 'To' → {{1.email}}, 'Subject' → 'New Deal {{1.title}}', 'Body' → маппинг полей сделки
- Фильтр-условия в Make.com: IF (deal_stage = 'Won') THEN (отправить уведомление), IF (deal_value > 5000) THEN (создать запись в CRM)
- Router/Iterator для обработки массивов: если Pipedrive возвращает список контактов, используйте Iterator для обработки каждого по отдельности
- Error Handling: aktivirovanie 'Continue on error' для пропуска фейлов, установка Fallback routes

## Ключевые инсайты
- API Token в Pipedrive имеет вид: 123abc456def789ghi — он уникален для каждого пользователя и хранит права доступа, никогда не делитесь им публично.
- Make.com поддерживает как Real-time webhooks так и polling (опрос API через интервалы) — Real-time работает через Pipedrive Webhooks Settings в админ-панели.
- При маппинге полей используйте {{module_number.field_name}} синтаксис, например {{1.deal_id}} для доступа к ID сделки из первого модуля.
- Лимиты API Pipedrive: 2 запроса в секунду для бесплатного плана, платные планы имеют выше лимиты — это влияет на frequency в Make.com workflows.
- Для работы с custom fields в Pipedrive используйте поле 'Custom Fields IDs' в Trigger, иначе custom поля не будут выведены в маппинге.
- Тестирование workflow обязательно на sandbox или test-сделке — используйте 'Run once' в Make.com, проверьте Execution logs для дебага.
- Batch processing: если нужно обработать 1000+ контактов, используйте Make.com 'Repeater' или 'Iterator' для batch-запросов с pagination.
- Ошибка 401 (Unauthorized) чаще всего означает невалидный API Token — проверьте его в Pipedrive Settings → Personal Preferences → API.
- При удалении сделок из Pipedrive используйте архивирование (soft delete) чтобы не потерять history в Make.com workflows.

## Подводные камни
_Не упомянуты_
