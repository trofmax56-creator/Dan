---
source: YouTube / Business Workflow
date: 2026-04-25
original: https://youtube.com/watch?v=AMnX-mfQZk4
category: GOLD
tags: [Make.com, SmartLead, Attio, ChatGPT, API, Lead Management, CRM, automation, workflow, Webhook, JSON, no-code]
extracted_by: Claude Haiku
---

## Суть
Автоматизация в Make.com для передачи лидов из SmartLead в Attio когда контактная информация отсутствует, с использованием ChatGPT для обработки данных лидов.

## Бизнес-сценарий
Компании, работающие с лидами в SmartLead, которые нуждаются в автоматическом экспорте лидов в Attio (CRM/платформу управления контактами) даже когда отсутствует контактная информация. Система интеллектуально обрабатывает неполные данные через ChatGPT и отправляет структурированные лиды в Attio.

## Алгоритм реализации
1. 1. Триггер: новый лид добавлен в SmartLead (webhook или polling из SmartLead API) — инициирует рабочий процесс
2. 2. Модуль получения данных лида: извлекаются поля лида (name, company, email, phone и т.д.) из SmartLead
3. 3. Проверка условия: если контактная информация (email, phone) отсутствует или неполная — активируется специальный блок обработки
4. 4. Модуль ChatGPT: отправляется промпт с информацией лида (только имя, компания и другие доступные данные) для получения рекомендаций по обработке или заполнению пробелов
5. 5. Трансформация данных: результат от ChatGPT структурируется согласно схеме Attio (mapping полей)
6. 6. Отправка в Attio: структурированные данные лида передаются через Attio API в соответствующий контакт/лид-модуль
7. 7. Логирование результата: фиксируется статус успешной отправки или ошибки для отчёта

## Технический стек
- Make.com (платформа автоматизации)
- SmartLead API (источник лидов)
- Attio API (целевая CRM)
- ChatGPT API (обработка неполных данных)
- Webhook (для триггера)
- JSON (формат данных)
- HTTP-модули Make.com
- Текстовые трансформаторы Make.com

## Связки инструментов
- SmartLead webhook → Make.com trigger
- Make.com → SmartLead API (data retrieval)
- Make.com → ChatGPT API (data enrichment)
- ChatGPT response → Make.com data mapper
- Make.com → Attio API (lead creation/update)
- Attio → Make.com (confirmation webhook)

## Конфигурация и параметры
- Триггер в Make.com: модуль 'SmartLead' с событием 'Watch New Lead' или webhook с URL вида https://hook.make.com/...
- SmartLead API endpoint: вероятно /api/v1/leads/{leadId} для получения деталей
- ChatGPT модуль: API ключ (Settings → API keys), модель 'gpt-3.5-turbo' или 'gpt-4', температура 0.7-1.0
- Промпт для ChatGPT: примерно 'Given a lead with incomplete contact info: {{name}}, {{company}}, suggest how to handle this lead or provide missing contact fields if possible'
- Attio API endpoint: /api/v1/contacts или /api/v1/leads, метод POST
- Mapping полей: SmartLead name → Attio name, SmartLead company → Attio company, ChatGPT suggestions → Attio custom fields
- Условие для пропуска: IF email is empty AND phone is empty THEN use ChatGPT, ELSE direct mapping
- Error handling: модуль 'Try-Catch' для обработки случаев когда API недоступны

## Ключевые инсайты
- 1. Использование ChatGPT позволяет не блокировать лиды с неполной информацией, а умно их обрабатывать
- 2. SmartLead часто предоставляет имя компании и/или имя контакта, даже без email/phone — это уже полезно для ChatGPT
- 3. Attio может хранить доп. поля (custom fields) с результатами анализа ChatGPT для последующей ручной обработки
- 4. Необходимо использовать Attio API v1 с правильной структурой JSON для POST-запроса создания контакта
- 5. Рекомендуется добавить логирование каждого шага (через функцию Make.com Scenarios → Logs) для отладки проблем с отсутствующими данными
- 6. Кэширование результатов ChatGPT для одинаковых компаний сокращает расходы и время обработки
- 7. Установить таймаут для ChatGPT запроса (макс 30 сек) чтобы избежать зависания workflow
- 8. Проверить rate limits SmartLead (обычно 100 req/min) и Attio (обычно 50-200 req/min) перед запуском на боевом

## Подводные камни
- ⚠️ SmartLead может возвращать null для email/phone вместо пустой строки — нужна проверка типа данных (IF data.email != empty AND data.email != null)
- ⚠️ Attio требует обязательное поле 'name' при создании контакта, иначе вернёт 400 ошибку
- ⚠️ ChatGPT API ограничивает текстовый размер входа (макс ~2000 token в базовых планах) — не отправлять большие описания
- ⚠️ Rate limiting: если отправлять много лидов одновременно, Attio API может вернуть 429 Too Many Requests — добавить задержку (Sleep модуль) между запросами
- ⚠️ SmartLead и Attio используют разные форматы для номеров телефонов (со страной или без) — нужна нормализация через регулярные выражения
- ⚠️ Если в SmartLead стоит флаг 'Do Not Contact', это должно быть заблокировано перед отправкой в Attio — добавить условие
- ⚠️ Бесплатные планы ChatGPT API могут быть заблокированы после определённого количества запросов в день (обычно 3-5 за 24ч) — требуется оплаченный аккаунт
- ⚠️ Attio webhook для подтверждения создания контакта может прийти с задержкой (до 5 мин) — не полагаться на синхронную обработку
