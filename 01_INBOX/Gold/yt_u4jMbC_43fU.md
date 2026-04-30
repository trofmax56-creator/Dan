---
source: YouTube / Business Workflow
date: 2026-04-14
original: https://youtube.com/watch?v=u4jMbC_43fU
category: GOLD
tags: []
extracted_by: Claude Haiku
status: archive
reason: low_score
score: Pain=5 Dev=7 Profit=5 ИТОГ=17
---

## Суть
Автоматизированный workflow для анализа положительных ответов на email-кампании: извлечение данных из SmartLead, обогащение в Attio, и AI-анализ ответов в Make.com для определения готовности лидов к продаже.

## Бизнес-сценарий
Sales/marketing специалисты и agency владельцы используют workflow для автоматизации обработки входящих ответов на cold-email кампании. Система анализирует тон и содержание ответов через AI, определяет качественные лиды и синхронизирует данные между SmartLead (платформа для email-кампаний), Attio (CRM для работы с контактами) и Make.com (оркестрация рабочего процесса).

## Алгоритм реализации
1. Шаг 1: Настройка триггера в Make.com — прослушивание webhook от SmartLead. При получении нового ответа на кампанию (reply) инициируется workflow. Параметр триггера: Watched Event = 'Email Reply'
2. Шаг 2: Парсинг входящих данных из SmartLead webhook. Извлечение полей: email отправителя (lead_email), содержание ответа (reply_body), тема письма (reply_subject), метаданные кампании (campaign_id, lead_id)
3. Шаг 3: Отправка текста ответа в Claude AI (через API) для анализа тональности и определения качества лида. Промпт AI: 'Analyze if this email reply indicates positive interest in our service. Return: sentiment (positive/negative/neutral), confidence (0-100), reason'
4. Шаг 4: Логический фильтр в Make.com — проверка результата AI анализа. Условие: если sentiment = 'positive' AND confidence > 70, продолжить workflow, иначе завершить
5. Шаг 5: Получение или создание контакта в Attio CRM через API. Поиск существующего контакта по email, если не найден — создание нового с полями: Name, Email, Lead Status, Campaign Source
6. Шаг 6: Обновление контакта в Attio новыми данными: добавление тега 'Positive Reply', сохранение текста ответа в кастомное поле Reply_Text, установка статуса 'Qualified Lead'
7. Шаг 7: Дополнительное обогащение данных через внешний API (опционально). Поиск информации о компании лида через Hunter.io или аналог для получения должности и размера компании
8. Шаг 8: Отправка уведомления в Slack/Email о новом квалифицированном лиде с кратким резюме анализа (email лида, вывод AI, ссылка на контакт в Attio)

## Технический стек
- Make.com (Integromat) — платформа для оркестрации и автоматизации
- SmartLead — платформа для холодных email-кампаний с webhook интеграцией
- Attio CRM — облачная CRM система для управления контактами и сделками
- Claude API (Anthropic) — AI модель для анализа текста и определения тональности
- Webhook — для синхронизации данных между SmartLead и Make.com
- REST API — для взаимодействия с Attio и Claude
- JSON — формат данных для передачи между сервисами

## Связки инструментов
- SmartLead Webhook → Make.com (Trigger)
- Make.com → Claude API (AI Text Analysis)
- Make.com Logic → Conditional Router (Positive/Negative)
- Make.com → Attio API (Contact Search/Create)
- Make.com → Attio API (Contact Update)
- Make.com → Slack API (Notification) или Email модуль

## Конфигурация и параметры
- Make.com Trigger настройка: URL вебхука для SmartLead, прослушивание события 'Email Reply'
- Поле в Make.com для парсинга SmartLead: {{trigger.reply_body}} — содержание ответа, {{trigger.lead_email}} — email адрес лида
- Claude API интеграция: endpoint 'https://api.anthropic.com/v1/messages', Authorization header с API ключом, модель 'claude-3-sonnet-20240229'
- Attio API базовый URL: 'https://api.attio.com/v1/people', требует API Key в header 'Authorization: Bearer YOUR_API_KEY'
- Make.com Router модуль: условие = {{sentiment}} == 'positive' && {{confidence}} > 70
- Attio контакт поля для обновления: custom_field_reply_text, custom_tag_positive_reply, status = 'Qualified Lead'
- Slack уведомление формат: текст с использованием переменных {{lead_email}}, {{ai_reason}}, {{attio_contact_url}}

## Ключевые инсайты
- Webhook от SmartLead срабатывает в реальном времени — ответы анализируются в течение секунд, что позволяет быстро реагировать на горячие лиды
- AI анализ через Claude позволяет избежать ложноположительных срабатываний за счет анализа контекста, а не простого ключевого слова
- Confidence score важен для фильтрации: порог 70% исключает сомнительные случаи, но может потребовать настройки под специфику бизнеса
- Двусторонняя синхронизация с Attio обеспечивает полноту данных — все лиды с положительными ответами автоматически попадают в CRM с нужными тегами
- Использование кастомных полей в Attio (Reply_Text) позволяет сохранять полный контекст взаимодействия для последующего анализа и коммуникации
- Webhook URL из Make.com должен быть добавлен в SmartLead settings для каждой кампании — проверяйте в документации SmartLead раздел 'Integrations'
- Опциональное обогащение через Hunter.io добавляет коммерческую ценность, помогая продажам быстро найти контактного лицо в целевой компании
- Slack уведомления снижают response time — команда видит квалифицированного лида не дожидаясь, пока кто-то проверит CRM вручную

## Подводные камни
_Не упомянуты_
