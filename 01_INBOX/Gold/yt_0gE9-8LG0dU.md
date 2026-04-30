---
source: YouTube / Business Workflow
date: 2026-04-14
original: https://youtube.com/watch?v=0gE9-8LG0dU
category: GOLD
tags: [make.com, smartlead, attio, CRM, automation, API, webhook, Claude, ChatGPT, AI, email-marketing, lead-scoring]
extracted_by: Claude Haiku
status: archive
reason: low_score
score: Pain=5 Dev=7 Profit=5 ИТОГ=17
---

## Суть
Автоматизация обработки положительных ответов на email-кампании из SmartLead в Attio CRM через Make.com с использованием AI для анализа эмоционального тона письма.

## Бизнес-сценарий
Sales-команды используют SmartLead для массовых email-кампаний. При получении ответа от потенциального клиента система автоматически анализирует текст письма через AI, определяет позитивный ответ, и создаёт контакт в Attio CRM с указанием статуса интереса. Это экономит время на ручную обработку и позволяет фокусироваться на горячих лидах.

## Алгоритм реализации
1. 1. SmartLead генерирует webhook при получении ответа на письмо (trigger в Make.com), передавая данные: email отправителя, текст ответа, ID кампании
2. 2. Make.com получает webhook и извлекает текст письма (поле 'reply_text' или 'body')
3. 3. Текст отправляется в Claude API (или GPT) для анализа эмоционального тона - нод 'Ask Claude' или 'Run Script' с промптом на определение позитивного ответа
4. 4. AI возвращает результат (true/false или оценку от 0 до 1) - является ли ответ положительным
5. 5. Условный блок (router или if-else) проверяет результат анализа
6. 6. Если ответ позитивный: Create Contact в Attio CRM с полями: email, name, status='Interested', source='SmartLead', campaign_id, reply_preview
7. 7. Если ответ негативный или нейтральный: либо игнорируется, либо создаётся с другим статусом
8. 8. Webhook отправляется обратно в SmartLead для логирования результата (опционально)

## Технический стек
- Make.com (Integromat) - платформа автоматизации
- SmartLead CRM - система для массовых email-кампаний
- Attio CRM - облачная CRM для управления контактами
- Claude API (Anthropic) или OpenAI GPT API - AI для анализа текста
- Webhook - для получения данных из SmartLead
- REST API - для интеграции с Attio и Claude
- JavaScript / Node.js - возможно для трансформации данных в Make.com

## Связки инструментов
- SmartLead Webhook → Make.com Webhook Receiver
- Make.com → Claude API / OpenAI (Ask Claude node)
- Claude Response (JSON parse) → Router/Condition Check
- Router True Branch → Attio CRM 'Create Contact' node
- Attio Response → Webhook back to SmartLead (optional logging)

## Конфигурация и параметры
- SmartLead: настроить webhook URL в разделе Integrations/Webhooks, указать событие 'reply_received'
- Make.com Webhook node: URL вида https://hook.make.com/[unique-id], Method: POST, Accept любой Content-Type
- Claude node: Model: claude-3-sonnet, Temperature: 0.3 (для консервативного анализа), Prompt шаблон: 'Analyze if this email reply shows positive interest: [reply_text]. Answer: true/false'
- Attio CRM node: Требуется API Key (Settings → API), Base URL: api.attion.com/v1 или https://api.attio.com/v1
- Attio Create Contact: Обязательные поля - email, name (может быть пусто), опциональные - status, tags, source
- Router node условие: {{1.data.sentiment}} === 'positive' или {{1.data.score}} > 0.7
- Headers для API запросов: Authorization: Bearer [API_KEY], Content-Type: application/json

## Ключевые инсайты
- SmartLead отправляет webhook данные сырыми - требуется парсинг JSON в Make.com через модуль 'Parse JSON'
- Claude стоит дешевле GPT-4 (~$0.003 за запрос vs $0.03) при аналогичной точности для анализа эмоционального тона
- Фильтр на уровне Make.com (не создавать контакты с отрицательными ответами) снижает нагрузку на Attio API и экономит платежи
- Оптимально добавить дедупликацию по email в Attio - перед созданием контакта проверить его существование через search endpoint
- Если SmartLead отправляет HTML письмо - нужно очищать теги через regex или встроенный модуль 'String' → 'Strip HTML'
- Рекомендуется логировать все ответы AI (даже если низкая уверенность) в отдельную таблицу Google Sheets для аудита и обучения модели
- Время выполнения каждого цикла: ~2-3 сек (webhook + API вызовы) - достаточно для real-time реакции на ответы

## Подводные камни
- Частая ошибка: SmartLead может отправлять поле 'reply' вместо 'reply_text' - проверить в документации SmartLead или тестировать webhook
- Attio CRM API требует наличия workspace_id в некоторых эндпоинтах - если запросы падают с 401/403, добавить это поле в заголовок
- Claude может интерпретировать нейтральные письма как позитивные (напр. 'Thanks for reaching out') - рекомендуется threshold выше 0.8
- Webhook в Make.com требует повторной активации при переходе между FREE и платными планами - может нарушить интеграцию
- Если письма приходят с копией (CC/BCC), SmartLead может отправить несколько вебхуков на один контакт - нужна дедупликация по ID
- Attio отклонит запрос если поле 'email' некорректное (не RFC 5322) - требуется валидация regex на этапе Make.com
- Лимиты API: SmartLead ~1000 req/мин, Claude ~1M токенов/мин, Attio ~100 req/мин при базовом плане - нужна очередь при пиках
