---
source: YouTube / _неизвестно_
date: _неизвестно_
original: https://youtube.com/watch?v=0AD3JktQqr8
category: GOLD
tags: []
extracted_by: Claude Haiku
---

## Суть
Развертывание Codex CLI на VDS (Virtual Dedicated Server) для автоматизации браузерных операций с помощью AI агента. Позволяет запускать интеллектуальные скрипты на выделенном сервере без локального браузера, получая результаты через CLI интерфейс.

## Бизнес-сценарий
DevOps инженеры, автоматизаторы и разработчики используют Codex CLI для развертывания AI агентов на VDS. Агент автоматизирует браузерные задачи (навигация по сайтам, заполнение форм, сбор данных), работает на удаленном сервере, результаты получаются через командную строку. Данные: URL сайтов, команды навигации, данные форм, результаты скрапинга.

## Алгоритм реализации
1. Шаг 1: Подготовка VDS — арендуем выделенный сервер (Linux/Ubuntu), получаем доступ по SSH, проверяем наличие Docker и необходимых зависимостей
2. Шаг 2: Установка Codex CLI — клонируем репозиторий, устанавливаем зависимости Python (pip install -r requirements.txt), генерируем API ключ для доступа к AI моделям
3. Шаг 3: Конфигурация окружения — создаём .env файл с переменными (CODEX_API_KEY, VDS_HOST, PORT), настраиваем параметры подключения к браузеру (Chromium/Firefox), выставляем таймауты и лимиты ресурсов
4. Шаг 4: Развертывание браузера на сервере — устанавливаем Chromium или Firefox в headless режиме, настраиваем Puppeteer/Playwright для работы с браузером через CLI, проверяем доступность через localhost:3000
5. Шаг 5: Создание первого AI агента — пишем конфиг агента (JSON с описанием задач), указываем инструкции для AI (какие действия совершать на сайтах), задаём примеры входных данных и ожидаемых выходов
6. Шаг 6: Тестирование агента локально — запускаем codex-agent test --config agent.json, проверяем логи на ошибки, убеждаемся что браузер открывается и закрывается корректно
7. Шаг 7: Развертывание на VDS — загружаем конфиг на сервер через SFTP/SCP, запускаем агент фоновым процессом (screen или systemd), настраиваем логирование в файл
8. Шаг 8: Интеграция с внешними системами — настраиваем webhook для запуска агента по событиям, подключаем результаты к API (например n8n, zapier), автоматизируем получение результатов через cron задачи

## Технический стек
- Codex CLI
- VDS (Virtual Dedicated Server)
- Linux/Ubuntu Server
- Docker
- SSH
- Python 3.8+
- Chromium/Firefox
- Puppeteer или Playwright
- headless браузер режим
- Node.js (для работы Puppeteer)
- curl/wget для API запросов
- .env для переменных окружения
- JSON для конфигурации агентов
- systemd/screen для фоновых процессов
- SFTP/SCP для передачи файлов
- bash скрипты

## Связки инструментов
- SSH → VDS → Docker → Codex CLI
- VDS Shell → codex-agent CLI → Chromium headless → результаты JSON
- Webhook/Event → Codex API → Chromium → скрапинг данных → HTTP Response
- cron → bash скрипт → codex-agent execute → результаты → webhook callback

## Конфигурация и параметры
- API ключ Codex в .env файле: CODEX_API_KEY=sk-xxxxx
- Порт браузера: PORT=3000 или 9222 (default для Chrome DevTools Protocol)
- Параметры браузера: --headless --no-sandbox --disable-dev-shm-usage
- Путь к Chromium: /usr/bin/chromium-browser или /snap/bin/chromium
- Таймауты: TIMEOUT=30000 (миллисекунды), PAGE_LOAD_TIMEOUT=15000
- Конфиг агента в JSON: { name, description, instructions, inputs: [{name, type}], outputs: [{name, type}] }
- Параметр режима: --mode headless или --mode debug
- Логирование: LOG_LEVEL=debug, LOG_FILE=/var/log/codex-agent.log
- Ограничение ресурсов Docker: memory=512m, cpus=1
- Webhook URL для результатов: WEBHOOK_URL=https://your-server.com/callback

## Ключевые инсайты
- Headless браузер экономит ресурсы на 60-70% по сравнению с обычным браузером благодаря отключению GUI
- Используй screen или tmux для persistent сессий на VDS — процесс не прерывается при разрыве SSH подключения
- Всегда выставляй --no-sandbox флаг при запуске Chromium в контейнере, иначе браузер не запустится
- Кэшируй результаты браузера в Redis или SQLite чтобы не переделывать одинаковые запросы
- Добавь rate-limiting (задержки между запросами) чтобы не получить бан от целевых сайтов
- Настрой logrotate для логов чтобы они не занимали всё место на диске VDS
- Используй Playwright вместо Puppeteer если нужна поддержка Firefox и Safari
- Создай systemd сервис для автозагрузки агента при перезагрузке VDS

## Подводные камни
- Браузер не запускается на VDS без --no-sandbox флага — это нормально, нужно его выставить
- SSH timeout при долгих операциях браузера — используй screen/tmux или запусти через &
- Недостаточно памяти для Chromium — выставляй --disable-dev-shm-usage чтобы использовать диск вместо /dev/shm
- API лимиты Codex — проверь план подписки, не все модели доступны по умолчанию
- Cloudflare и другие антибот системы блокируют автоматические запросы — добавь User-Agent и задержки между действиями
- Пути к бинарникам отличаются в разных дистрибутивах Linux — используй which chromium-browser или find /usr -name chromium
- Docker в Docker может быть нестабилен на некоторых VDS — проверь kernel версию
- Webhook callback может упасть если результаты слишком большие — добавь compression и streaming
