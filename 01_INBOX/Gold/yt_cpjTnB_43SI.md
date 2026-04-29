---
source: YouTube / RAI Studio
date: 2026-03-05
original: https://youtube.com/watch?v=cpjTnB_43SI
category: GOLD
tags: []
extracted_by: Claude Haiku
---

## Суть
Создание WhatsApp AI-агента с помощью n8n и Meta API для автоматизации бизнес-коммуникаций. Агент получает сообщения через Meta WhatsApp Cloud API, обрабатывает их AI-моделью (Claude/GPT), и отправляет ответы обратно в WhatsApp, полностью автоматизируя взаимодействие с клиентами.

## Бизнес-сценарий
Компании используют решение для автоматизации WhatsApp поддержки: система получает входящие сообщения клиентов, передаёт их в AI-модель для генерации ответа, автоматически отправляет обработанный ответ клиенту без участия человека. Это экономит время операторов и обеспечивает 24/7 поддержку.

## Алгоритм реализации
1. Шаг 1: Регистрация и настройка Meta WhatsApp Cloud API на developer.facebook.com. Создание Business App, получение номера телефона для WhatsApp Business и API токена (обычно формат: EAAx...)
2. Шаг 2: Настройка Webhook в Meta API для получения входящих сообщений. Указать URL webhook (обычно URL n8n вебхука) и подтвердить токен (verify token)
3. Шаг 3: Создание workflow в n8n. Добавить ноду Webhook для получения входящих сообщений от Meta. Webhook должен слушать POST-запросы с data[0].message для текстовых сообщений
4. Шаг 4: Добавить ноду AI (Claude, ChatGPT, Gemini) для обработки текста сообщения. Передать в ноду содержимое сообщения (обычно {{ $json.entry[0].changes[0].value.messages[0].text.body }}) и получить AI-ответ
5. Шаг 5: Добавить ноду HTTP Request для отправки ответа обратно в Meta WhatsApp API. Использовать endpoint POST https://graph.instagram.com/v18.0/{PHONE_NUMBER_ID}/messages с параметрами: messaging_product=whatsapp, to={CUSTOMER_NUMBER}, type=text, text.body={AI_RESPONSE}. Авторизация через Bearer Token (API токен Meta)
6. Шаг 6: Тестирование: отправить тестовое сообщение на WhatsApp номер, проверить что workflow триггеризуется, AI генерирует ответ и сообщение доходит обратно пользователю

## Технический стек
- n8n — платформа для автоматизации workflows
- Meta WhatsApp Cloud API (v18.0 и выше) — API для получения и отправки сообщений
- Claude API / ChatGPT API / Gemini API — AI модель для генерации ответов
- Webhook (HTTP POST) — для получения входящих сообщений
- HTTP Request ноды в n8n — для синхронизации с внешними API
- Evolution API (опционально) — альтернатива для интеграции WhatsApp
- JSON обработка в n8n — парсинг структуры сообщений Meta

## Связки инструментов
- Meta Webhook → n8n Webhook нода → получение входящих сообщений
- n8n → Claude/ChatGPT API ноды → обработка текста AI
- n8n HTTP Request → Meta WhatsApp Cloud API (POST /messages) → отправка ответа
- Входящее сообщение структура: entry[0].changes[0].value.messages[0].text.body
- Исходящее сообщение структура: { messaging_product: 'whatsapp', to: CUSTOMER_NUMBER, message: { type: 'text', text: { body: AI_RESPONSE } } }

## Конфигурация и параметры
- Meta App ID и App Secret — получить в Facebook Developers Console
- PHONE_NUMBER_ID — номер телефона WhatsApp Business (например, 1234567890123)
- API Token — персональный токен доступа Meta (Bearer Token для Authorization header)
- Verify Token (webhook token) — произвольная строка для подтверждения webhook (можно любая, например: my_webhook_secret_123)
- Webhook URL в n8n — должна быть публичная URL вида https://your-n8n-domain.com/webhook/whatsapp
- API версия Meta — рекомендуется v18.0 или выше
- Номер телефона клиента (CUSTOMER_NUMBER) — извлекается из entry[0].changes[0].value.messages[0].from
- Сообщение от клиента (MESSAGE_BODY) — находится в entry[0].changes[0].value.messages[0].text.body
- Claude API Key, ChatGPT API Key или Gemini API Key — для выбранной AI модели

## Ключевые инсайты
- Meta WhatsApp API работает асинхронно через Webhook. Все входящие сообщения приходят POST-запросом на указанный webhook URL, а не через polling
- Структура JSON от Meta вложена глубоко: нужно правильно парсить entry[0].changes[0].value.messages[0] для получения текста сообщения и номера отправителя
- API токен Meta имеет срок действия (обычно 60 дней). Нужно настроить автоматическое обновление токена или использовать долгоживущий токен (long-lived token)
- При отправке сообщения через Meta API обязательно указывать messaging_product=whatsapp и правильный PHONE_NUMBER_ID (это ID номера бизнеса, не персональный номер клиента)
- Rate limiting в Meta API: обычно 60 сообщений в минуту бесплатно, выше нужна подписка. Нужно добавить обработку ошибки 429 (Too Many Requests)
- Для надёжности добавить обработку ошибок: если AI API недоступна, отправить автоматический ответ вроде 'Я временно недоступна, напишу позже'
- Meta требует одобрение шаблонов сообщений для каждого бизнеса. Первый ответ без использования шаблона может быть отклонён
- Webhook должна быть доступна 24/7 и отвечать в течение 5 секунд. n8n автоматически хостит webhook, если использовать встроенные Webhook-ноды
- Для безопасности хранить API токены в переменных среды (Environment Variables) n8n, не в plain text в workflow
- Тестирование можно проводить с Test Contact номером Meta (обычно +1-550-555-0199), на который Meta разрешает отправлять сообщения без одобрения

## Подводные камни
_Не упомянуты_
