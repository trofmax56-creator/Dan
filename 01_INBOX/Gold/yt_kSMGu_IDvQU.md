---
source: YouTube / Tutorials With Noel
date: 2026-04-21
original: https://youtube.com/watch?v=kSMGu_IDvQU
category: GOLD
tags: []
extracted_by: Claude Haiku
---

## Суть
Автоматизация сбора лидов из Facebook Lead Ads и их синхронизация с Google Sheets через платформу Make.com без необходимости писать код. Это позволяет компаниям в реальном времени получать данные потенциальных клиентов в электронную таблицу, исключая ручной ввод и ошибки.

## Бизнес-сценарий
Компании, использующие Facebook Lead Ads для генерации лидов, нуждаются в автоматическом сохранении контактной информации в Google Sheets для последующей обработки, анализа и интеграции с CRM-системами. Это процесс работает для: - Агентства по недвижимости, собирающие заявки от потенциальных покупателей - E-commerce предприятия, получающие контакты подписчиков - B2B компании, ловящие lead-маршруты через рекламу

## Алгоритм реализации
1. Шаг 1: Создание сценария в Make.com - Залогиниться в аккаунт Make.com (make.com), нажать 'Create New Scenario' или 'New scenario', назвать проект (например, 'Facebook Leads to Google Sheets 2026')
2. Шаг 2: Добавление триггера Facebook Lead Ads - Нажать на иконку '+' для добавления модуля, выбрать 'Facebook' из списка приложений, выбрать триггер 'New Lead' или 'Webhooks - Instant' для Facebook Lead Ads, авторизоваться с Facebook Business Account, выбрать рекламный аккаунт и форму для сбора лидов (Lead Form ID)
3. Шаг 3: Тестирование триггера - Нажать 'Run once' или 'Choose where to start' для тестирования подключения, создать тестовый лид в Facebook Lead Ads форме, убедиться что данные поступают в Make.com (должны отобразиться поля: Full Name, Email, Phone, Custom Fields и т.д.)
4. Шаг 4: Добавление модуля Google Sheets - После триггера нажать '+' и добавить новый модуль, выбрать 'Google Sheets' из списка приложений, выбрать действие 'Add a Row', авторизоваться с Google-аккаунтом, выбрать нужную spreadsheet и sheet/вкладку
5. Шаг 5: Маппинг полей из Facebook в Google Sheets - В каждом поле Google Sheets модуля выставить соответствие с полями из триггера Facebook (используя переменные из левой колонки). Например: Column A (Name) ← Full Name (из Facebook), Column B (Email) ← Email (из Facebook), Column C (Phone) ← Phone Number, Column D (Lead Date) ← Created Date/Timestamp из триггера Facebook Lead Ads
6. Шаг 6: Настройка дополнительных полей и фильтров (опционально) - Добавить фильтр если нужно обрабатывать только лиды из определенного региона или с конкретными параметрами, использовать функции преобразования данных (например, CONCATENATE для объединения имени и фамилии), установить условия на полях (IF statements)
7. Шаг 7: Активация сценария - Нажать кнопку 'Turn on' в левом верхнем углу, убедиться что статус сценария изменился на 'Enabled' (зеленый индикатор), протестировать создав еще один лид через Facebook Lead Ads форму и проверив его появление в Google Sheets
8. Шаг 8: Мониторинг и управление - Использовать раздел 'Executions' в Make.com для мониторинга каждого запуска сценария, проверить логи на предмет ошибок, если есть failed execution, нажать на него для отладки и просмотра причины сбоя

## Технический стек
- Make.com (платформа для no-code автоматизации)
- Facebook Lead Ads API (для получения данных из форм лидов)
- Google Sheets API (для добавления строк в таблицы)
- Webhook (если используется типа 'Webhooks - Instant')
- Facebook Business Manager (для управления рекламными кампаниями и формами лидов)

## Связки инструментов
- Facebook Lead Ads Form → Make.com Webhook/Trigger → Google Sheets API → New Row Addition
- Facebook Business Account Authentication → Lead Form Selection → Field Mapping → Google Sheets Column Mapping

## Конфигурация и параметры
- Триггер Facebook: выбрать 'New Lead' или 'Webhooks - Instant', подтвердить список полей (Full Name, Email, Phone, Custom Fields, Created At timestamp)
- Lead Form ID: найти в Facebook Ads Manager → Assets → Forms, скопировать ID формы
- Google Sheets модуль: выбрать Spreadsheet ID (из URL: docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit), выбрать Sheet Name (например, 'Sheet1' или 'Leads')
- Маппинг полей: Column A → Full Name; Column B → Email; Column C → Phone; Column D → Lead Date (можно использовать formatDate для преобразования timestamp); Column E → Additional Info (если есть custom fields)
- Дополнительные параметры: 'Add a row' модуль имеет опцию 'Location' - выбрать 'End of the list', опция 'Include Column Headers' если нужны заголовки
- Google Sheets авторизация: требуется доступ 'Google Sheets' scope с permission на редактирование (write)

## Ключевые инсайты
- Facebook Lead Ads API предоставляет данные в реальном времени, но требует наличия Facebook Business Account с активными Lead Ads кампаниями
- Make.com использует 'mapping' панель слева - это переменные из триггера, которые нужно перетаскивать в поля модулей, а не вводить текст вручную
- При маппинге email и phone полей проверить что они не null в Facebook форме, иначе Google Sheets получит пустые значения
- Сценарий в Make.com работает асинхронно - лид появляется в Google Sheets с задержкой 1-5 секунд после заполнения Facebook формы
- Если используется 'Webhooks - Instant' вместо стандартного триггера, нужно скопировать webhook URL в Facebook Lead Ads конфигурацию для real-time синхронизации
- Google Sheets имеет лимит API quota (300 requests per minute) - при большом объеме лидов (500+ в час) рекомендуется добавить aggregator модуль для батчинга
- При первом подключении Facebook, Make.com просит выбрать рекламный аккаунт (Ad Account) - выбрать тот, где находится нужная Lead Ads форма
- Для отладки использовать опцию 'Inspect' в Make.com на любом модуле чтобы увидеть точные JSON-структуры данных, которые передаются между модулями

## Подводные камни
_Не упомянуты_
