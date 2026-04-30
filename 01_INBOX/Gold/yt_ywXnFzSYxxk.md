---
source: YouTube / Business Workflow
date: 2026-04-15
original: https://youtube.com/watch?v=ywXnFzSYxxk
category: GOLD
tags: []
extracted_by: Claude Haiku
status: archive
reason: low_score
score: Pain=5 Dev=7 Profit=5 ИТОГ=17
---

## Суть
Автоматизация анализа входящих писем из SmartLead CRM в Attio CRM с использованием ChatGPT для определения положительных ответов на кампании холодного контакта. Рабочий процесс интегрирует SmartLead и Attio через Make.com с AI-анализом для фильтрации и квалификации лидов.

## Бизнес-сценарий
Sales-команды и SMM-агентства, которые ведут кампании холодного контакта через SmartLead, получают огромное количество писем с ответами на рассылки. Нужно автоматически отделить положительные ответы от отказов и спама, затем отправить их в Attio CRM для дальнейшей обработки и следующих шагов продаж.

## Алгоритм реализации
1. Шаг 1: Настройка триггера в Make.com — выбираем SmartLead как исходный приложение. Создаём вебхук или используем встроенный модуль SmartLead для отслеживания новых ответов на письма из кампаний.
2. Шаг 2: Получение данных письма — подключаемся к API SmartLead, извлекаем текст ответного письма, email отправителя, название кампании, статус ответа из полей: message_body, sender_email, campaign_name, reply_status.
3. Шаг 3: Обращение к ChatGPT API — передаём текст письма в ChatGPT (модель gpt-3.5-turbo или gpt-4) с промптом: 'Проанализируй это письмо и определи, является ли ответ: 1) Положительным (интерес к предложению), 2) Отрицательным (отказ), 3) Нейтральным (просьба не писать). Ответь одним словом: POSITIVE, NEGATIVE или NEUTRAL'.
4. Шаг 4: Условное разветвление (IF-условие) — проверяем результат от ChatGPT. Если ответ содержит 'POSITIVE', переходим на шаг 5. Иначе переходим на шаг 6 (для отрицательных/нейтральных записываем в отдельный сценарий или пропускаем).
5. Шаг 5: Отправка в Attio CRM — используем модуль Attio, создаём новый контакт или обновляем существующий с полями: email, company_name, source='SmartLead', status='Positive Reply', message=полный текст ответа, created_at=текущая дата. API эндпоинт: POST /contacts или PATCH /contacts/{id}.
6. Шаг 6: Логирование отрицательных ответов (опционально) — для отказов и нейтральных ответов можно создать отдельный лог в Google Sheets или Airtable, или просто завершить выполнение без добавления в Attio.
7. Шаг 7: Проверка ошибок — добавляем error handling: если ChatGPT недоступен, письмо содержит не-текстовый формат или SmartLead не вернул корректные данные, записываем ошибку в логи и уведомляем администратора через Slack или email.

## Технический стек
- Make.com (сервис автоматизации, платформа орхестрации)
- SmartLead CRM (исходное приложение для отслеживания кампаний холодного контакта)
- Attio CRM (целевое приложение для управления контактами и сделками)
- ChatGPT API (OpenAI API для анализа текста писем)
- Вебхуки (для передачи данных между системами)
- Google Sheets или Airtable (опционально, для логирования)
- Slack API (опционально, для уведомлений об ошибках)

## Связки инструментов
- SmartLead вебхук → Make.com триггер (получение нового письма)
- Make.com → ChatGPT API (анализ содержимого письма)
- ChatGPT результат → Условная логика в Make.com (IF POSITIVE)
- Make.com → Attio CRM API (создание/обновление контакта)
- Make.com → Google Sheets / Slack (логирование и уведомления)

## Конфигурация и параметры
- SmartLead модуль: выбрать триггер 'Watch Replies' или 'New Reply', настроить фильтр по статусу 'replied' или 'unread'
- Поля из SmartLead: email, first_name, last_name, company, message_text, campaign_id, created_at, reply_date
- ChatGPT промпт: точно сформулировать инструкцию — 'Determine if this email is positive interest (POSITIVE), rejection (NEGATIVE), or unsubscribe request (NEUTRAL). Reply with single word.'
- API ключ ChatGPT: должен быть сохранён в переменных окружения Make.com как {{chatgpt_api_key}}
- Attio модуль: выбрать 'Create Contact' или 'Update Contact', маппировать поля: {{email}} → email, {{first_name}} → first_name, {{company}} → company_name, {{message_text}} → custom_field_reply, {{sender_email}} → email
- HTTP-статус коды: 200 (успех), 400 (ошибка в данных), 401 (неавторизованный доступ), 429 (лимит запросов к API), 500 (ошибка сервера)
- Rate limiting: ChatGPT имеет ограничения по количеству запросов (3500 RPM для pay-as-you-go), нужно добавить delay между запросами или использовать очередь
- Attio API format: используется REST API с JSON payload, обязательные заголовки: Authorization: Bearer {{attio_api_token}}, Content-Type: application/json
- SmartLead API dokumentacija: используется REST API с аутентификацией через API-ключ в заголовке 'Authorization: Bearer {{smartlead_api_key}}'
- Make.com функции: можно использовать {{lower()}} для приведения результата ChatGPT к нижнему регистру перед проверкой, {{trim()}} для удаления пробелов

## Ключевые инсайты
_Нет данных_

## Подводные камни
_Не упомянуты_
