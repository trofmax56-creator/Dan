---
source: YouTube / Quick Learn Team
date: 2026-04-29
original: https://youtube.com/watch?v=tRvNhDhM1Hw
category: GOLD
tags: []
extracted_by: Claude Haiku
---

## Суть
Автоматизация WhatsApp с помощью Make.com для потокового взаимодействия с клиентами через бизнес-сообщения и интеграцию ИИ с целью снижения ручного управления коммуникациями и повышения скорости ответов.

## Бизнес-сценарий
Бизнес-пользователи, SaaS-компании, агентства и фрилансеры используют Make.com для автоматизации входящих сообщений WhatsApp, маршрутизации обращений, генерации ответов через ИИ (Claude, ChatGPT, Gemini) и синхронизации данных с CRM (Bitrix24, amoCRM, Google Sheets).

## Алгоритм реализации
1. Шаг 1: Установка и подключение Make.com акаунта. Регистрация на platform make.com, переход в раздел 'Scenarios', создание нового сценария (Create a new scenario).
2. Шаг 2: Добавление триггера WhatsApp. В левой панели сценария нажимается иконка '+', выбирается интеграция 'WhatsApp Business API' или 'WhatsApp Integration' (в зависимости от версии Make.com). Затем выбирается событие 'Watch Messages' или 'New Incoming Message'.
3. Шаг 3: Настройка подключения WhatsApp Business. Требуется указать Webhook URL (генерируется Make.com автоматически), Phone Number ID (получается из Facebook Business Manager), Access Token (получается из Meta-приложения WhatsApp Business). В WhatsApp Business API settings указывается Webhook URL для получения входящих сообщений.
4. Шаг 4: Добавление модуля ИИ для обработки текста. Добавляется модуль 'AI (ChatGPT, Claude, Gemini)' - можно выбрать любой из доступных провайдеров. Параметры: Model (GPT-4, Claude 3 Opus и т.д.), Temperature (0.5-0.7 для баланса творчества и консистентности), Max tokens (500-2000 в зависимости от типа ответа), Prompt/System message (описание роли и инструкции ИИ-ассистента).
5. Шаг 5: Извлечение данных сообщения из триггера. Используются переменные триггера: {{body}} (текст сообщения), {{from}} (номер отправителя), {{timestamp}} (время сообщения), {{messageId}} (уникальный ID сообщения). Эти значения передаются в промпт ИИ-модуля.
6. Шаг 6: Отправка сгенерированного ответа через WhatsApp. Добавляется модуль 'Send Message' интеграции WhatsApp Business. Параметры: To (номер получателя {{from}}), Message Type (text/template), Message Content ({{output}} от ИИ-модуля), Phone Number ID, Access Token.
7. Шаг 7: Интеграция с CRM для сохранения переписки. Добавляется модуль для записи (например, 'Bitrix24 - Create Lead' или 'Google Sheets - Add Row'). Поля: Contact Number ({{from}}), Message Text ({{body}}), AI Response ({{output}}), Timestamp ({{timestamp}}). Это создаёт историю взаимодействия.
8. Шаг 8: Добавление условной логики (Router/Conditional). Используется модуль 'Router' для распределения сообщений по типам: If contains 'support' → направить support-специалисту; If contains 'sales' → передать в отдел продаж; Otherwise → ответить автоматически. Условия настраиваются через 'Text Contains', 'Regular Expression Match', 'Conditions'.
9. Шаг 9: Тестирование сценария. Нажимается кнопка 'Run once' для запуска тестового прогона с реальными данными. Проверяются логи выполнения (View logs, Check each module output). Если ошибки — исправляются параметры модулей.
10. Шаг 10: Активация сценария. После успешного тестирования сценарий активируется (кнопка 'Turn on'), становится live, и начинает обрабатывать входящие сообщения в реальном времени.

## Технический стек
- Make.com (workflow automation platform)
- WhatsApp Business API (Meta/Facebook)
- Claude API / ChatGPT API / Google Gemini API (ИИ-генерация ответов)
- Bitrix24 API (опционально, для синхронизации контактов и лидов)
- amoCRM API (опционально, для управления сделками)
- Google Sheets API (опционально, для логирования сообщений)
- Webhook (для приёма входящих сообщений из WhatsApp)
- JSON (формат обмена данными между модулями)
- JavaScript / Regular Expression (для обработки условий и форматирования текста)

## Связки инструментов
- Webhook (входящие сообщения) → Make.com (обработка) → Claude/ChatGPT API (генерация ответа) → WhatsApp Business API (отправка) → Получатель
- WhatsApp Business API → Make.com Webhook → Router (условная логика) → [Support Queue / CRM / Auto-Response]
- WhatsApp Message ({{from}}, {{body}}, {{timestamp}}) → ИИ-модуль → CRM/Google Sheets (запись истории) → WhatsApp Send Module → Customer

## Конфигурация и параметры
_Нет данных_

## Ключевые инсайты
_Нет данных_

## Подводные камни
_Не упомянуты_
