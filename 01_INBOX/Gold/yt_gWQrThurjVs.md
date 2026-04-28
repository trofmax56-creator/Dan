---
source: YouTube / Business Workflow
date: 2026-04-16
original: https://youtube.com/watch?v=gWQrThurjVs
category: GOLD
tags: []
extracted_by: Claude Haiku
---

## Суть
Автоматизация передачи контактов из SmartLead в CRM Attio с использованием Make.com для анализа статусов "Do not contact" и синхронизации данных контактов между платформами.

## Бизнес-сценарий
Агентства и отделы B2B-продаж используют эту автоматизацию для синхронизации результатов холодного аутрича из SmartLead в Attio CRM, чтобы автоматически разделять контакты с кампаний на две категории: интересующихся и отклонивших (Do not contact), исключая таким образом мёртвые контакты из дальнейшего обрабатывания.

## Алгоритм реализации
1. Шаг 1: Создать Webhook триггер в Make.com для приёма данных из SmartLead. Выбрать модуль 'Webhooks' → 'Custom Webhook' → скопировать URL вебхука для вставки в SmartLead
2. Шаг 2: Настроить SmartLead на отправку контактов в вебхук Make.com при завершении кампании. В SmartLead: Automations → Create Automation → Webhook Trigger → вставить URL из Make.com → выбрать параметры отправки (контакты, статусы, email)
3. Шаг 3: В Make.com добавить фильтр для анализа поля 'Do not contact' статуса контакта. Использовать модуль Filter → условие: if contact.status = 'Do not contact' → then skip this contact, else continue
4. Шаг 4: Добавить HTTP модуль для получения дополнительных данных контакта из Attio API (если требуется проверка дубликатов). Настроить GET запрос с параметрами: endpoint = 'https://api.attio.com/v2/records', параметр 'email' = значение из SmartLead
5. Шаг 5: Создать модуль Attio ('Attio' → 'Create Record' или 'Update Record') для записи контакта в CRM. Маппировать поля: SmartLead.email → Attio.Email, SmartLead.firstName → Attio.First Name, SmartLead.lastName → Attio.Last Name, SmartLead.company → Attio.Company, SmartLead.status → Attio.Lead Status
6. Шаг 6: Добавить модуль 'Router' или условие 'IF' для разветвления логики: контакты со статусом 'Do not contact' отправлять в отдельный список в Attio или пропускать полностью. Контакты с активными статусами отправлять на создание/обновление records
7. Шаг 7: Настроить обработку ошибок с помощью Error Handler: при ошибке API Attio логировать результат в Google Sheets или отправлять уведомление. Добавить модули для retry-логики при timeout
8. Шаг 8: Протестировать workflow с тестовым контактом из SmartLead, убедиться что данные корректно маппируются и контакты появляются в Attio с правильными статусами и полями

## Технический стек
- Make.com (автоматизационная платформа)
- SmartLead (платформа для холодного аутрича и email-маркетинга)
- Attio CRM (система управления контактами)
- Webhooks (для передачи данных в реальном времени)
- Attio API v2
- HTTP модули для REST запросов
- JSON парсинг для обработки данных контактов

## Связки инструментов
- SmartLead Webhook → Make.com Custom Webhook
- Make.com Router/Filter → условная логика для анализа 'Do not contact'
- Attio API v2 (HTTP модуль) → проверка дубликатов и получение ID records
- Make.com Attio Native Connector → Create/Update Record в CRM
- Error Handler → Google Sheets логирование или Slack notifications

## Конфигурация и параметры
- Webhook URL из Make.com вставляется в SmartLead под: Automations → Webhook Settings
- HTTP запрос к Attio API требует заголовок Authorization: Bearer [API_KEY] (получить в Attio Settings → API Tokens)
- Маппирование полей SmartLead → Attio: проверить точные названия полей в обоих системах (например, 'firstName' в SmartLead может быть 'first_name' в Attio)
- Фильтр в Make.com проверяет наличие статуса 'Do not contact' в поле contact.status или в отдельном флаге
- Attio Record Type должен быть выбран (обычно 'Person' для контактов или 'Company' для организаций)
- При использовании Router: левый путь (true) → обработка контактов, правый путь (false) → логирование или пропуск
- Retry-настройки в Make.com: Max retries = 3, Retry interval = 5 seconds
- Таймаут для HTTP запросов: 30 секунд

## Ключевые инсайты
_Нет данных_

## Подводные камни
_Не упомянуты_
