---
source: YouTube / Сергей Чербаджи
date: 2026-04-29
original: https://youtube.com/watch?v=wIF2HGGHGc0
category: GOLD_CRM
tags: []
extracted_by: Claude Haiku
---

## Суть
Полный курс по n8n для создания бизнес-автоматизаций и ИИ-интеграций без необходимости написания кода. Охватывает 23 урока от базовых концепций до продвинутых сценариев с искусственным интеллектом, позволяя автоматизировать рутинные бизнес-процессы и интегрировать ИИ-инструменты в workflow.

## Бизнес-сценарий
Для бизнес-аналитиков, маркетологов, предпринимателей и разработчиков, которые хотят автоматизировать повторяющиеся задачи (обработка данных, интеграция CRM/Email-сервисов, обработка заказов, управление контентом), интегрировать ИИ-модели (ChatGPT, Claude, Gemini) в свои процессы без написания кода.

## Алгоритм реализации
1. Шаг 1: Установка и первичная настройка n8n — развёртывание локально или в облаке, доступ к интерфейсу, изучение основного Layout (левая панель с Nodes, центр — рабочий холст, правая панель — параметры)
2. Шаг 2: Создание первого простого workflow — добавление тригера (например, Webhook или Schedule), подключение нескольких базовых нод (HTTP Request, Set, Switch, Merge)
3. Шаг 3: Подключение внешних сервисов и API — настройка интеграций с популярными платформами (Bitrix24, amoCRM, Gmail, Slack), создание и управление API-ключами в credentials
4. Шаг 4: Работа с условной логикой и обработкой данных — использование нод Switch для условных ветвлений, Set для трансформации данных, Function для пользовательской логики на JavaScript
5. Шаг 5: Интеграция ИИ-моделей — подключение ChatGPT, Claude, Gemini через их API, создание prompt-инженерии, обработка ответов от ИИ
6. Шаг 6: Обработка ошибок и отладка — использование Error Handling, логирование результатов, тестирование каждого шага workflow, Debug информация
7. Шаг 7: Продвинутые сценарии — создание сложных workflow с циклами (Loop), параллельной обработкой (Merge), работой с базами данных, хранением истории операций

## Технический стек
- n8n (основная платформа автоматизации)
- REST API / HTTP Request (интеграция с внешними сервисами)
- Webhooks (триггеры из внешних источников)
- ChatGPT API / OpenAI
- Claude API (Anthropic)
- Google Gemini API
- Bitrix24 API
- amoCRM API
- Gmail API
- Slack API
- JavaScript/JSON (для функций и трансформации данных)
- SQLite / PostgreSQL (если работа с БД)
- JSON парсинг и манипуляция
- Cron expressions (для Schedule нод)
- OAuth2 (для авторизации в сервисах)

## Связки инструментов
- Webhook (входящий) → n8n Trigger → HTTP Request (к ChatGPT API) → Set (трансформация результата) → Slack (отправка сообщения)
- Schedule (ежедневно) → HTTP Request (к Bitrix24 API) → Switch (условное ветвление) → amoCRM Update (если условие верно) / Email (если нет)
- Gmail Webhook → n8n → Claude API → Set (парсинг ответа) → Database Save → Email ответ
- Form Submission Webhook → Function (validate & prepare) → ChatGPT (генерация контента) → Bitrix24 (создание сделки) → Slack notification
- Schedule → HTTP Request (fetch данные) → Loop (обработка каждого элемента) → ИИ обработка → Database insert

## Конфигурация и параметры
- Nodes Left Panel: список всех доступных нод (Trigger, Action, Transform, Combine, Tools, Flow)
- Trigger нод: Webhook (слушает входящие HTTP POST), Schedule (расписание по Cron), Email Trigger, Form Trigger
- HTTP Request нода: Method (GET/POST/PUT), URL (эндпоинт), Headers (авторизация, Content-Type), Body (параметры запроса), Authentication (Basic, OAuth2, API Key)
- Set нода: поле Expression Editor для JavaScript выражений, { new_field: '{{$node.previous_node.json.field}}' } синтаксис
- Switch нода: условия (Routing Rules), например 'data.status == paid' → ветка A, else → ветка B
- Credentials: правый верхний угол → Credentials → New → выбрать тип (API Key, OAuth2, Basic Auth) → сохранить
- API Key в Credentials: название, ключ, базовый URL (если требуется)
- Function нода: JavaScript код в текстовой области, возврат JSON объекта, доступ к предыдущим данным через $node.node_name.json
- Schedule нода: Cron expression (0 9 * * 1 = каждый понедельник в 9:00), Timezone выбор
- Email/Slack/Telegram нода: заполнение полей To/From/Subject/Message, использование {{$node.name.json.field}} для вставки данных
- Loop нода: Item name (переменная для текущего элемента), Array expression (источник данных)
- Merge нода: type (Add, Extend, Replace), точка слияния нескольких веток

## Ключевые инсайты
_Нет данных_

## Подводные камни
_Не упомянуты_
