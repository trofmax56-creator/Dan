---
source: YouTube / Игорь Зуевич
date: 2026-02-08
original: https://youtube.com/watch?v=9sor5jfqLGs
category: GOLD
tags: [n8n, Claude API, Claude Code, Python, Execute Python, HTTP Request, API интеграция, автоматизация, AI-агент, код-генерация, Webhook, workflow, без кода, low-code]
extracted_by: Claude Haiku
status: ideas_lab
score: Pain=6 Dev=7 Profit=6 ИТОГ=19
---

## Суть
Упрощение создания n8n-автоматизаций в 10 раз за счёт интеграции Claude Code (генерация Python-кода) без необходимости ручного программирования. Claude API генерирует готовый Python-код, который встраивается в n8n Execute Python node для автоматизации сложных операций.

## Бизнес-сценарий
Разработчики и операторы n8n используют Claude Code для генерации Python-скриптов, которые обрабатывают сложные бизнес-логики (преобразование данных, интеграции API, обработка текстов). Это позволяет создавать мощные автоматизации без глубоких знаний программирования, экономя время на разработку и тестирование.

## Алгоритм реализации
1. 1. Запуск n8n и создание нового Workflow (пустой Canvas)
2. 2. Добавление триггера (Webhook, Manual trigger или другой источник данных)
3. 3. Вставка ноды 'Execute Python' из палитры ассоциаций
4. 4. Добавление ноды 'HTTP Request' для отправки запроса к Claude API с промптом на Python
5. 5. В HTTP Request настроить: URL = https://api.anthropic.com/v1/messages (или актуальный эндпоинт), метод POST, заголовок Authorization: Bearer YOUR_CLAUDE_API_KEY, body с моделью claude-3-5-sonnet и системным промптом на генерацию Python-кода
6. 6. Настроить mapping: передавать данные из предыдущей ноды в промпт для Claude
7. 7. Обработать ответ от Claude в Execute Python ноде - распарсить JSON, выделить код из content[0].text
8. 8. Выполнить сгенерированный Python-код в Execute Python ноде с помощью eval() или exec()
9. 9. Маппировать входные данные (переменные workflow) в контекст выполнения Python
10. 10. Добавить завершающую ноду (например, Update item в Bitrix24 или сохранение результата) для получения выходных данных от Python

## Технический стек
- n8n (версия 1.x+)
- Claude API (Anthropic)
- Python 3.x (встроенный в n8n Execute Python)
- HTTP Request ноды n8n
- Execute Python ноды n8n
- JSON парсинг
- Webhook для триггеров
- Anthropic SDK / REST API

## Связки инструментов
- Webhook (входящие данные) → n8n HTTP Request → Claude API (генерация Python) → Ответ парсится в JSON → Execute Python (выполнение кода) → Обновление данных в CRM/БД
- n8n Execute Python → Локальные переменные workflow → input data → обработка → $json output

## Конфигурация и параметры
- HTTP Request к Claude API: URL = https://api.anthropic.com/v1/messages
- Заголовок: Content-Type: application/json, Authorization: Bearer {CLAUDE_API_KEY}
- Body JSON: {"model": "claude-3-5-sonnet", "max_tokens": 2000, "messages": [{"role": "user", "content": "Write Python code to: [описание задачи]"}], "system": "You are a Python code generator..."}
- Execute Python: импорты нужных библиотек (requests, json, datetime и т.д.) в начало скрипта
- Mapping переменных: {{ $json.input_field }} внутри Python-кода для доступа к данным workflow
- Обработка ответа Claude: response = JSON.parse(http_response); code = response.content[0].text; exec(code)

## Ключевые инсайты
- Claude Code позволяет писать Python с помощью естественного языка - достаточно описать задачу, Claude сам сгенерирует готовый работающий код
- Экономия времени: вместо 2-3 часов на написание скрипта вручную - минуты на описание и генерацию
- Python-код в n8n имеет доступ ко всем встроенным библиотекам: requests, json, datetime, re, math и т.д.
- Стоимость Claude API (0.003 USD за 1K input tokens) несоизмеримо ниже, чем оплата труда разработчика на написание скрипта
- Итеративное улучшение: если код не работает, перепроси Claude с уточнениями - будет быстрее, чем дебаг вручную
- Типичная топология: Webhook → Validate data → Call Claude API → Parse response → Execute Python → Update/Send data
- Важно использовать переменные workflow ({{ $json.field_name }}) внутри Claude-промпта, чтобы контекст был правильный
- Execute Python ноде можно передавать результаты предыдущих нод через {{ $node.http_request.json.content[0].text }}
- Необходимо escaping кавычек и спецсимволов при передаче данных в Claude-промпт через JSON
- Для production используй версионирование промптов и тестирование на различных входных данных

## Подводные камни
- ОПАСНОСТЬ: eval() и exec() уязвимы для произвольного кода - Claude может случайно вернуть опасный код, всегда проверяй output перед исполнением
- Лимит токенов Claude API: если Python-код большой, он может обрезаться - установи max_tokens достаточно большим (2000-4000)
- Время выполнения: вызов Claude API занимает 1-3 секунды на запрос, что медленнее обычного Python-скрипта в n8n
- Стоимость: частые вызовы Claude для одного и того же кода будут иметь накопляющуюся стоимость - кэшируй результаты
- Версионирование моделей: Claude API меняется (claude-3-5-sonnet, claude-3-opus и т.д.), убедись что используешь актуальную версию
- JSON парсинг ответа: формат ответа от Claude может немного отличаться в зависимости от версии API - всегда добавляй обработку ошибок
- Python окружение n8n: не все внешние библиотеки установлены по-умолчанию - используй встроенные (requests, json, etc.)
- Спецсимволы в промпте: кавычки, апострофы, новые строки могут сломать JSON - используй proper escaping
- Отсутствие интернета: если n8n не может подключиться к Claude API, workflow упадёт - добавь retry-логику
- Логирование и дебаг: используй console.log() или print() для отладки, результаты смотри в n8n execution logs
