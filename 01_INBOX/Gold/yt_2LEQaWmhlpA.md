---
source: YouTube / Guilherme Lazarotto - Tecnologia & Automação
date: 2026-04-03
original: https://youtube.com/watch?v=2LEQaWmhlpA
category: GOLD_CRM
tags: []
extracted_by: Claude Haiku
---

## Суть
Полная интеграция Evolution GO (API для WhatsApp) с платформой n8n для автоматизации работы с WhatsApp. Видео охватывает установку Evolution GO и её подключение к n8n для создания автоматизированных workflows с использованием новой WhatsApp API (2026 версия).

## Бизнес-сценарий
Компании и фрилансеры, которые нужно автоматизировать обработку WhatsApp сообщений, интегрировать WhatsApp с системами CRM, рассылки и управления контактами. Решение обрабатывает входящие сообщения, управляет контактами через API, отправляет автоматические ответы и синхронизирует данные между WhatsApp и внешними сервисами.

## Алгоритм реализации
1. Шаг 1: Установка Evolution GO на сервер — развертывание Docker контейнера или Node.js приложения Evolution GO, настройка портов (по умолчанию 8080), конфигурация переменных окружения (API_KEY, INSTANCE_NAME)
2. Шаг 2: Получение API ключей Evolution GO — после запуска сервиса получить/сгенерировать API token через веб-интерфейс Evolution на localhost:8080, скопировать API URL и API key для дальнейшего использования
3. Шаг 3: Создание инстанса WhatsApp в Evolution GO — через админ-панель Evolution создать новый instance (экземпляр подключения), указать параметры: имя инстанса, webhook URL для получения входящих сообщений
4. Шаг 4: Подключение аккаунта WhatsApp к Evolution — отсканировать QR-код в Evolution интерфейсе для авторизации WhatsApp аккаунта (как в mWeb), дождаться статуса 'connected'
5. Шаг 5: Создание New Workflow в n8n — открыть n8n интерфейс, создать новый workflow, добавить триггер (webhook или polling) для получения данных от Evolution GO
6. Шаг 6: Настройка HTTP Request ноды в n8n для Evolution API — добавить HTTP Request ноду с методом GET/POST, установить URL: https://[evolution-server]:8080/message/sendText, передать параметры: instance_name, api_key, number (номер получателя), text (текст сообщения)
7. Шаг 7: Настройка webhook для входящих сообщений — в Evolution указать webhook URL вида https://[n8n-server]/webhook/evolution-incoming, n8n будет получать POST запросы с данными сообщений и контактов
8. Шаг 8: Добавление логики обработки — использовать Switch/If ноду в n8n для условной обработки сообщений, например: проверка типа сообщения, отправка ответа, сохранение в БД
9. Шаг 9: Интеграция с CRM или БД — добавить ноду (например, Bitrix24, Postgres, Google Sheets) для сохранения контактов и истории сообщений из WhatsApp
10. Шаг 10: Тестирование и мониторинг — отправить тестовое сообщение на WhatsApp номер, проверить выполнение workflow в n8n logs, убедиться что данные корректно передаются между системами

## Технический стек
- Evolution GO — API сервис для управления WhatsApp
- n8n — платформа автоматизации (self-hosted или cloud)
- Docker — для контейнеризации Evolution GO
- Node.js — runtime для Evolution GO
- WhatsApp API (новая версия 2026) — интеграция с WhatsApp
- HTTP/REST API — для коммуникации между Evolution и n8n
- Webhook — для получения входящих событий
- QR-код сканирование — авторизация WhatsApp аккаунта
- Возможна интеграция: Bitrix24, amoCRM, Google Sheets, Postgres, MySQL для сохранения данных

## Связки инструментов
- Evolution GO WebHook → n8n HTTP Request → API эндпоинты Evolution для отправки сообщений
- WhatsApp → Evolution GO (через QR-авторизацию) → n8n workflow → CRM/БД
- Входящее сообщение → Evolution Webhook → n8n Webhook триггер → Обработка логики → HTTP запрос обратно в Evolution для ответа

## Конфигурация и параметры
- Evolution GO API URL: https://[server-ip]:8080
- API Key: получить из админ-панели Evolution при создании application key
- Instance Name: имя подключения WhatsApp аккаунта (пример: 'main-account')
- HTTP Method: POST для отправки сообщений, GET для получения информации
- Endpoint для отправки: POST /message/sendText
- Параметры endpoint sendText: { instance: 'instance_name', number: '5511999999999' (номер с кодом страны), text: 'сообщение', delay: 1000 (задержка в мс) }
- Webhook URL в Evolution: должна быть публичная URL n8n webhook'а вида https://[domain]/webhook/webhook-name
- Webhook Events: message.create (входящее сообщение), status.update (изменение статуса доставки)
- Port Evolution GO: 8080 (по умолчанию, можно изменить в config)
- Авторизация: API key передается в header Authorization: Bearer [API_KEY] или в query параметре apikey

## Ключевые инсайты
- Evolution GO требует публичный IP или domain + SSL сертификат для работы webhook'ов с WhatsApp
- QR-код авторизации работает максимум 40-60 секунд, нужно быстро отсканировать в мобильном приложении WhatsApp
- При отправке сообщений номер телефона должен содержать код страны (55 для Бразилии) без символов (+, -, пробелы): 5511999999999
- API ключ Evolution нельзя сбрасывать после генерации — его нужно сохранить, т.к. пересоздать сложнее
- Задержка между сообщениями (delay параметр) обязательна, иначе WhatsApp заблокирует аккаунт за спам (рекомендуется 1000-3000 мс)
- В n8n используется {{ $json.data }} для доступа к полям из webhook payload от Evolution
- Evolution GO может работать в режиме polling (регулярные запросы) или webhook (real-time события) — webhook быстрее и надежнее
- Статус сообщения (delivered, read, failed) приходит через статус webhook, нужно обрабатывать для надежной доставки
- Если Evolution GO падает, все ждущие сообщения теряются — нужна логика повторных попыток в n8n
- Максимальный размер текста сообщения: 4096 символов, для больших объёмов нужно разбивать на части

## Подводные камни
_Не упомянуты_
