---
source: YouTube / Agentic Tech Flow
date: 2026-04-12
original: https://youtube.com/watch?v=pL8C5BttzRg
category: GOLD_CRM
tags: []
extracted_by: Claude Haiku
---

## Суть
Развертывание собственного языкового модели на VPS-сервере Hostinger как альтернатива подпискам на ChatGPT, что позволяет избежать ежемесячных платежей и обеспечивает полный контроль над данными.

## Бизнес-сценарий
Для разработчиков, стартапов и компаний, которые хотят использовать LLM (языковые модели) без ежемесячных подписок на OpenAI ChatGPT, с сохранением конфиденциальности данных и полной контролировать использование AI-моделей на собственной инфраструктуре.

## Алгоритм реализации
1. Шаг 1: Регистрация аккаунта на Hostinger и выбор VPS-плана (минимум 2GB RAM для базовых моделей, рекомендуется 4GB+)
2. Шаг 2: Развертывание операционной системы Linux (Ubuntu 22.04 LTS рекомендуется) на VPS через панель управления Hostinger
3. Шаг 3: Подключение по SSH к VPS-серверу через терминал: ssh root@[IP_АДРЕС_СЕРВЕРА]
4. Шаг 4: Установка Docker на сервер для контейнеризации: sudo apt update && sudo apt install docker.io docker-compose
5. Шаг 5: Установка и запуск Ollama (легкого фреймворка для локального запуска LLM) через Docker: docker run -d -p 11434:11434 ollama/ollama
6. Шаг 6: Загрузка языковой модели через Ollama CLI: ollama pull llama2 или ollama pull mistral
7. Шаг 7: Создание API-интеграции через expose портов и настройка reverse proxy (nginx) для безопасного доступа
8. Шаг 8: Подключение к локальной LLM через API endpoint http://[IP_СЕРВЕРА]:11434/api/generate
9. Шаг 9: Создание собственного приложения на Python или Node.js для обращения к LLM
10. Шаг 10: Мониторинг использования ресурсов (CPU, RAM, disk space) через Hostinger панель или htop утилиту на сервере

## Технический стек
- Hostinger VPS
- Linux Ubuntu 22.04 LTS
- Docker & Docker Compose
- Ollama (LLM Framework)
- Llama 2 или Mistral модели
- CUDA (опционально для GPU ускорения)
- nginx (Reverse Proxy)
- SSH
- Python (для клиентского приложения)
- API REST
- git

## Связки инструментов
- SSH Terminal → Hostinger VPS Linux
- Docker Container → Ollama Framework → LLM Model
- API Endpoint (http://IP:11434/api/generate) → Client Application
- nginx Reverse Proxy → External Access
- GitHub/Git Repository → Code Deployment on VPS

## Конфигурация и параметры
- Выбор VPS плана: базовый план Hostinger с минимум 2GB RAM, 2 vCPU, 20GB SSD
- ОС: Ubuntu 22.04 LTS Server Edition
- SSH порт: 22 (стандартный)
- Ollama API порт: 11434 (внутренний), может быть проксирован на 80/443
- Docker контейнер: ollama/ollama:latest
- Модель: llama2 (7B) или mistral (7B) для оптимального баланса скорости и качества
- nginx конфиг: proxy_pass http://localhost:11434 с настройкой SSL/TLS
- API endpoint метод: POST к /api/generate с JSON payload
- Параметры запроса к LLM: model, prompt, temperature, top_p, num_predict

## Ключевые инсайты
- Экономия: замена $20/мес подписки ChatGPT на $3-4/мес VPS Hostinger = 80% экономии
- Выбор модели критичен: Llama2 7B требует ~13GB VRAM, для 2GB сервера нужны квантизированные версии (Q4_K_M)
- Ollama автоматически скачивает и кэширует модели, уменьшая потребление памяти через квантизацию
- Для production: обязательно включить SSL/TLS сертификаты (Let's Encrypt) через nginx и настроить Rate Limiting
- Первый запрос к модели может занять 30-60 секунд (загрузка модели в VRAM), последующие быстрее за счет кэша
- Multimodal модели (с видео/изображениями) требуют GPU - без neuro accelerator будут работать медленно
- Backup важен: регулярно сохранять папку ~/.ollama где хранятся скачанные модели
- API документация Ollama доступна локально на http://localhost:11434/docs при запуске контейнера
- Для автоматизации: создать Webhook или cronjob для обновления моделей и мониторинга здоровья сервера
- Бесплатные альтернативы моделям: Mistral 7B быстрее Llama2, ORCA лучше для reasoning, Zephyr для диалогов

## Подводные камни
- ⚠️ Недостаточная память: если выделить менее 2GB RAM, контейнер will crash при загрузке полной модели - используй квантизированные версии Q4
- ⚠️ Старые версии Docker: убедись что Docker версии 20.10+, иначе портирование портов может не работать
- ⚠️ Firewall Hostinger: открыть порты в панели хостинга, иначе API будет недоступен извне - белый лист IP или открыть все входящие
- ⚠️ Скорость интернета сервера: первая загрузка Llama2 модели (~5GB) может занять 15-30 минут в зависимости от скорости
- ⚠️ VRAM vs Disk: не путай - модель займет VRAM во время запуска, но требует места на диске для хранения (~5GB для 7B модели)
- ⚠️ Множественные запросы: Ollama по умолчанию неблокирующий (async), но при >5-10 одновременных запросах будут timeout'ы - добавить очередь (Redis/RabbitMQ)
- ⚠️ SSL сертификат: если использовать http без HTTPS, клиентские браузеры заблокируют запросы по CORS - обязательна валидная SSL сертификация
- ⚠️ Перезагрузки сервера: контейнер Docker не запускается автоматически после перезагрузки - добавить restart policy: docker run --restart unless-stopped
