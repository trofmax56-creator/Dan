---
source: YouTube / Performance Marketer Man
date: 2026-04-20
original: https://youtube.com/watch?v=sZbhqlqmv4I
category: GOLD_CRM
tags: [n8n, Facebook Leads, WhatsApp Business API, automation, webhook, лид-менеджмент, CRM, ChatBot, интеграция, Hindi tutorial]
extracted_by: Claude Haiku
---

## Суть
Автоматизация отправки лидов из Facebook Leads в WhatsApp через n8n. Workflow перехватывает новые лиды из Facebook, обрабатывает их данные и автоматически отправляет сообщения в WhatsApp контактам потенциальных клиентов.

## Бизнес-сценарий
CRM и лид-менеджеры используют этот workflow для автоматической обработки лидов из Facebook рекламы. Система получает контактные данные клиентов (имя, телефон, email), валидирует их и отправляет приветственное сообщение в WhatsApp без ручного вмешательства.

## Алгоритм реализации
1. Шаг 1: Создание вебхука в n8n для получения данных из Facebook Lead Forms. Настроить триггер 'Webhook' с методом POST и скопировать URL для добавления в Facebook Pixel/Lead Forms
2. Шаг 2: Добавление ноды 'HTTP Request' для получения доп. информации о лиде из Facebook API (используя Lead ID и Access Token)
3. Шаг 3: Парсинг полученных данных - извлечение имени, телефона, email из объекта лида с помощью Expression Editor
4. Шаг 4: Валидация номера телефона - проверка формата номера и добавление страны-кода (например +91 для Индии). Использование условной ноды (IF) для проверки наличия номера
5. Шаг 5: Отправка сообщения в WhatsApp через n8n ноду 'WhatsApp Business API' или через HTTP Request к WhatsApp API. Настройка шаблонной переменной с именем лида: 'Hello {{name}}, thank you for your interest...'
6. Шаг 6: Логирование результатов - отправка данных в Google Sheets или Airtable для отслеживания отправленных сообщений и статуса доставки. Настройка обработки ошибок и повторных попыток отправки

## Технический стек
- n8n (workflow automation platform)
- Facebook Lead Forms / Facebook Pixel
- Facebook Graph API (для получения данных лидов)
- WhatsApp Business API
- HTTP Request (для API вызовов)
- Expression Editor (для обработки данных)
- Google Sheets или Airtable (для логирования)
- Webhook (входящее соединение)

## Связки инструментов
- Facebook Lead Form Webhook → n8n Webhook Trigger → Parse Data (Expression) → Validate Phone → WhatsApp Business API → Google Sheets Logging
- n8n Workflow: Webhook (POST) → HTTP Request (Facebook Graph API) → Conditional Node → WhatsApp Send Message Node → Result Logger

## Конфигурация и параметры
- Webhook URL из n8n скопировать в Facebook Ads Manager > Lead Form Settings > Webhook URL
- Facebook Access Token получить из Facebook App > Settings > Developers
- WhatsApp Business API Credentials: Phone Number ID и Access Token из Meta Business Manager
- Expression для парсинга имени из лида: $json.first_name
- Expression для номера телефона: '{{\$json.phone_number}}'
- Условие в IF ноде: $json.phone_number != null && $json.phone_number != ''
- Сообщение WhatsApp содержит переменную: 'Hello {{first_name}}, thanks for contacting us!'
- Настройка retry policy: максимум 3 попытки отправки с интервалом 5 секунд
- Google Sheets интеграция: Append Row с колонками 'Lead Name', 'Phone', 'Message Status', 'Timestamp'

## Ключевые инсайты
- Facebook Lead Form отправляет webhook в n8n в JSON формате с массивом полей lead_data[]
- Телефонные номера из Facebook часто приходят без страна-кода, требуется добавить +91 для индийских номеров или использовать автоопределение
- WhatsApp API требует предварительно одобренные шаблоны сообщений, нельзя отправлять случайный текст
- Для первого сообщения используется template message, для последующих нужна инициация сессии от клиента
- Лучше добавить sleep ноду на 2-3 секунды между получением лида и отправкой в WhatsApp для избежания rate limit ошибок
- Обязательно логировать все ошибки доставки (failed, invalid_phone, rate_limit) для анализа проблем
- Meta требует использование только одобренные номера отправителя, добавить номер в WhatsApp Business Account Settings
- При отправке на неверный формат номера WhatsApp API возвращает 400 ошибку, заранее валидировать через регулярное выражение

## Подводные камни
- Webhook URL должен быть HTTPS, HTTP не работает - скопировать точный URL из n8n
- Facebook требует verify token при первом запросе к webhook, n8n не всегда генерирует его автоматически
- Если лид не содержит номер телефона, workflow зависнет или отправит некорректное сообщение - обязательна валидация перед отправкой
- Rate limiting: WhatsApp позволяет примерно 1000 сообщений в день для нового номера, позже лимит увеличивается
- Access Token из Facebook имеет ограниченное время жизни, требует refresh или использование long-lived token
- При переводе скрипта на production: обновить App Mode с 'Development' на 'Production' в Meta App Dashboard
- Если используется HTTP Request вместо встроенной WhatsApp ноды, нужно правильно структурировать JSON payload с messaging_product: 'whatsapp'
