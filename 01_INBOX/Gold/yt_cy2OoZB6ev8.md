---
source: YouTube / Noor Chatmize
date: 2026-04-23
original: https://youtube.com/watch?v=cy2OoZB6ev8
category: GOLD_CRM
tags: []
extracted_by: Claude Haiku
---

## Суть
Интеграция ManyChat с HubSpot через n8n для автоматического создания контактов и тикетов. Система получает данные из чатбота ManyChat и синхронизирует их в CRM HubSpot в реальном времени.

## Бизнес-сценарий
Маркетинговые команды и малые бизнесы используют ManyChat для общения с клиентами через Telegram/WhatsApp/Facebook, а HubSpot для управления контактами и CRM. Автоматизация создаёт в HubSpot новых контактов на основе данных из ManyChat и автоматически создаёт тикеты для обработки запросов.

## Алгоритм реализации
1. Шаг 1: Настройка вебхука в ManyChat — перейти в интеграции ManyChat, создать Custom Webhook с событием на сообщение пользователя, получить URL вебхука
2. Шаг 2: Создание workflow в n8n — новый workflow, добавить ноду 'Webhook' для приёма данных от ManyChat
3. Шаг 3: Парсирование данных из ManyChat — добавить ноду 'Function' или 'Set' для извлечения полей: subscriber_id, subscriber_name, phone, email, message_text из JSON-payload от ManyChat
4. Шаг 4: Поиск контакта в HubSpot — добавить ноду 'HubSpot CRM' с действием 'Search contacts by email', использовать поле email из payload ManyChat
5. Шаг 5: Условное ветвление (IF) — проверить результат поиска: если контакт найден, перейти к созданию тикета; если нет, создать новый контакт
6. Шаг 6: Создание нового контакта — если контакт не найден, использовать ноду 'HubSpot CRM' с действием 'Create contact', передать поля: email, firstname, lastname, phone, manyhat_subscriber_id (кастомное поле)
7. Шаг 7: Создание тикета в HubSpot — добавить ноду 'HubSpot CRM' с действием 'Create ticket', установить: subject (из message_text), description, связать с контактом (contact_id), установить статус 'open'
8. Шаг 8: Обработка ошибок — добавить ноды для логирования ошибок и уведомления в Slack при сбое интеграции
9. Шаг 9: Тестирование и активация — протестировать workflow отправкой сообщения в ManyChat, проверить создание контакта и тикета в HubSpot, активировать workflow

## Технический стек
- n8n (платформа автоматизации)
- ManyChat (чатбот для мессенджеров)
- HubSpot CRM API
- Webhook (для приёма данных)
- Custom integrations в ManyChat
- Function-ноды в n8n для обработки данных
- HTTP запросы для API вызовов

## Связки инструментов
- ManyChat Webhook → n8n Webhook ноду → HubSpot CRM API (поиск контакта) → Условное ветвление (IF) → Создание контакта/Создание тикета → HubSpot API

## Конфигурация и параметры
- URL вебхука n8n вида: https://your-n8n-domain.com/webhook/manychat
- Payload от ManyChat включает: subscriber (объект с id, name, phone, email), message (text), timestamp
- Аутентификация HubSpot: API token в формате Bearer authentication с токеном из HubSpot
- Кастомное поле в HubSpot для хранения subscriber_id: 'manyhat_subscriber_id' (type: text)
- Фильтр поиска контакта: search по email, если не найден — создать новый
- Mapping полей: ManyChat subscriber.name → HubSpot firstname/lastname (разбить по пробелу), ManyChat subscriber.phone → HubSpot phone, ManyChat subscriber.email → HubSpot email
- Статус тикета при создании: 'open'
- Приоритет тикета: может быть 'low', 'medium', 'high' (по умолчанию обычно 'medium')

## Ключевые инсайты
- ManyChat отправляет webhook при каждом новом сообщении — это рекомендуется ограничить только сообщениями от пользователей (не боте) через фильтры в ManyChat
- В HubSpot есть встроенные интеграции, но они часто не полностью кастомизируются — n8n позволяет создавать сложные логики типа 'создать контакт И тикет одновременно'
- API rate limiting у HubSpot: бесплатный план ~100 запросов в минуту, нужно добавлять задержки между массовыми операциями
- Важно не дублировать контакты — всегда проверяйте по email перед созданием (или по manyhat_subscriber_id)
- При сбое API HubSpot весь workflow зависает — используйте error handling ноды для retry логики
- Поле 'phone' в HubSpot имеет ограничения на формат — может требовать очистку данных (удаление спецсимволов)
- Тикеты в HubSpot могут быть привязаны только к контакту или компании — убедитесь, что contact_id передан корректно
- Вебхук в n8n имеет timeout ~30 секунд — если обработка дольше, используйте асинхронные ноды или разбивайте на несколько workflow'ов

## Подводные камни
- Если subscriber_name в ManyChat не разделён на firstname/lastname, нужна функция для парсирования (обычно первое слово = firstname, остальное = lastname)
- HubSpot требует уникальный email для контакта — дублирование приведёт к ошибке; используйте поиск перед созданием
- Webhook URL в n8n генерируется после сохранения workflow — убедитесь, что вы копируете правильный URL в ManyChat
- ManyChat может отправлять payload без email, если пользователь не заполнил профиль — добавьте условия для обработки пустых полей
- При изменении структуры payload от ManyChat весь workflow может сломаться — используйте логирование всех приходящих данных для отладки
- Если в HubSpot используется кастомный pipeline для тикетов, может потребоваться указать stage_id при создании
- ВАЖНО: API токен HubSpot должен быть сохранён в переменных окружения n8n (Credentials), а не в тексте workflow'а
