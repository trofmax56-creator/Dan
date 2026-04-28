---
source: YouTube / Игорь Зуевич
date: 2026-01-20
original: https://youtube.com/watch?v=VQEpvwHFhzI
category: GOLD
tags: []
extracted_by: Claude Haiku
---

## Суть
Автоматизация Telegram-бота с помощью искусственного интеллекта через n8n: за 7 минут настроить без кода webhook, подключить ИИ-модель (Claude, ChatGPT или Gemini) и организовать полностью функциональный chatbot, который обрабатывает входящие сообщения пользователей и отправляет ответы обратно в Telegram.

## Бизнес-сценарий
Телеграм-боты для бизнеса и контента: создание чат-ботов без программирования для автоматического ответа на вопросы, обработки заказов, поддержки клиентов или модерации. Работает для малого бизнеса, фрилансеров, авторов контента и команд, которые хотят автоматизировать коммуникацию в Telegram без написания кода.

## Алгоритм реализации
1. Шаг 1: Регистрация в n8n (n8n.io) — создать бесплатный аккаунт, войти в dashboard, начать новый workflow (Create Workflow или Add Workflow)
2. Шаг 2: Добавить первую ноду — 'Webhook' (найти в поиске): настроить HTTP метод на POST, сохранить webhook URL (он автоматически генерируется, вида https://n8n.io/webhook/xxxxxx)
3. Шаг 3: Скопировать Webhook URL и вставить его в настройки Telegram-бота (в BotFather команда /setwebhook [URL]) или через API Telegram методом setWebhook
4. Шаг 4: Добавить ноду для парсинга входящего сообщения — 'Function' или 'Set' ноду для извлечения текста сообщения из webhook payload (поле message.text или аналогичное в зависимости от структуры)
5. Шаг 5: Добавить ноду ИИ-модели (OpenAI/ChatGPT, Anthropic/Claude или Google/Gemini API) — настроить API ключ, модель, системный prompt и передать туда текст из Шага 4
6. Шаг 6: Добавить ноду 'Telegram' или HTTP запрос для отправки ответа ИИ обратно пользователю через Telegram API метод sendMessage (параметры: chat_id, text, parse_mode)
7. Шаг 7: Активировать workflow кнопкой 'Save and Activate' — workflow начнёт получать и обрабатывать сообщения в реальном времени, каждое сообщение пройдёт через весь pipeline и пользователь получит ответ ИИ

## Технический стек
- n8n (self-hosted или cloud, версия v1.x+) — платформа для no-code автоматизации
- Telegram Bot API (Telegram BotFather) — для создания и управления ботом
- OpenAI API / ChatGPT (или Claude API / Google Gemini API) — ИИ-модель для генерации ответов
- Webhook (HTTPS) — для получения входящих сообщений от Telegram
- HTTP клиент (встроенный в n8n) — для отправки запросов к Telegram и ИИ API
- JSON парсер — для обработки структурированных данных между сервисами
- Node.js runtime (если n8n self-hosted) — для выполнения workflow
- Database (SQLite или PostgreSQL в n8n) — опционально, для хранения истории сообщений

## Связки инструментов
- Webhook (входящее сообщение от Telegram) → n8n Webhook нода → Function/Set ноды для парсинга
- Распарсенный текст → OpenAI/Claude/Gemini API ноды → получение ответа ИИ
- Ответ ИИ → HTTP нода с Telegram sendMessage методом → отправка пользователю в Telegram

## Конфигурация и параметры
- Webhook ноды: HTTP Method = POST, URL генерируется автоматически (вида https://n8n.io/webhook/UUID), сохранить этот URL
- Telegram BotFather: команда /newbot для создания бота, получить TOKEN, затем /setwebhook чтобы привязать webhook URL к боту, или использовать API метод setWebhook
- OpenAI/Claude/Gemini ноды: вставить API Key (получить в личном кабинете), выбрать модель (gpt-4, gpt-3.5-turbo, claude-3-sonnet и т.д.), задать System Prompt (инструкция для ИИ), вставить User Message (текст от пользователя)
- Telegram sendMessage HTTP запрос: метод POST на https://api.telegram.org/botТОКЕН/sendMessage, параметры в JSON: { chat_id: '123456789', text: 'ответ ИИ', parse_mode: 'HTML' или 'Markdown' }
- Function ноды для парсинга: извлечь из webhook payload поле chat_id (для ответа) и message.text (текст сообщения), вывести как JSON { chatId, userMessage }
- Error Handling: добавить Try/Catch или условные ноды для обработки ошибок API (timeout, invalid key, rate limit)
- Активация: кнопка 'Save and Activate' в правом верхнем углу — workflow переходит в режим прослушивания webhook

## Ключевые инсайты
_Нет данных_

## Подводные камни
_Не упомянуты_
