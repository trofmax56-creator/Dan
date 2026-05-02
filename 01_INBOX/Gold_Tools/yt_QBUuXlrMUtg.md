---
source: YouTube / Kushal Vijay
date: 2026-05-02
original: https://youtube.com/watch?v=QBUuXlrMUtg
category: GOLD_TOOLS
tags: []
extracted_by: Claude Haiku
---

## Суть
Google запустила бесплатный 5-дневный курс по построению AI-агентов с использованием GenAI и Vertex AI. Курс обучает разработчиков созданию интеллектуальных агентов, которые могут самостоятельно принимать решения и выполнять сложные задачи через API и интеграции.

## Бизнес-сценарий
Разработчики и инженеры автоматизации учатся создавать AI-агентов на платформе Google Cloud. Агенты используют Gemini API для обработки текста, вызова инструментов (tool calling) и выполнения автоматизированных бизнес-процессов. Применимо для компаний, использующих Google Cloud, Vertex AI и нуждающихся в автоматизации сложных рабочих процессов через AI.

## Алгоритм реализации
1. Шаг 1: Зарегистрироваться на курс 'AI Agents: Intensive' на Google Cloud Console или через официальный портал обучения Google Cloud
2. Шаг 2: Настроить Google Cloud проект и включить необходимые APIs (Vertex AI API, Generative AI API)
3. Шаг 3: Аутентификация через Google Cloud SDK - установить gcloud CLI и выполнить 'gcloud auth login'
4. Шаг 4: Создать агента в Vertex AI - определить инструменты (tools/functions), которые агент может вызывать через tool calling
5. Шаг 5: Написать код на Python (или Node.js) с использованием Google GenAI SDK или Vertex AI Python client для инициализации агента
6. Шаг 6: Реализовать цикл взаимодействия агента - передача user input → обработка в Gemini API → выполнение инструментов → обновление состояния
7. Шаг 7: Интегрировать агента с внешними API и сервисами (CRM, базы данных, webhooks) через функции-инструменты (tool definitions)
8. Шаг 8: Развернуть агента на Vertex AI (serverless deployment) или Cloud Functions для использования в production
9. Шаг 9: Мониторить и логировать работу агента через Cloud Logging и Vertex AI Model Monitoring
10. Шаг 10: Пройти практические задания курса для закрепления знаний о создании многошаговых агентов

## Технический стек
- Google Vertex AI
- Google Gemini API
- Google Cloud Platform (GCP)
- Python 3.9+
- Google Cloud SDK (gcloud CLI)
- google-generativeai (Python library)
- google-cloud-vertexai (Python SDK)
- Tool Calling / Function Calling механизм
- Google Cloud Console
- Cloud Logging
- Cloud Monitoring
- Cloud Functions (опционально)
- REST API
- JSON (для определения инструментов)
- Node.js (альтернатива Python)

## Связки инструментов
- User Input → Gemini API (text-generation) → Tool Calling (определение необходимого инструмента) → External API/Function (выполнение) → Response Generation → User
- GCP Project Setup → Service Account Creation → Vertex AI API Enablement → Python SDK Installation → Agent Initialization
- Agent Code → Tool Definitions (JSON schema) → Gemini Process → Function Execution Loop → Output Formatting

## Конфигурация и параметры
- Google Cloud Project ID - уникальный идентификатор проекта в GCP
- Vertex AI API - включена в Cloud Console (APIs & Services > Library > поиск 'Vertex AI API')
- Generative AI API - также требует включения для использования Gemini моделей
- Model ID: 'gemini-1.5-pro' или 'gemini-1.5-flash' - названия моделей для инициализации агента
- Location: 'us-central1' или 'europe-west1' - регион развертывания Vertex AI
- Tool Definition Schema - JSON с описанием function_declarations (name, description, parameters)
- Authentication: Service Account JSON key file или Application Default Credentials (ADC)
- Rate limits и quotas - проверяются в Quotas & System Limits в Cloud Console

## Ключевые инсайты
- Google предоставляет бесплатный 5-дневный интенсив-курс с готовыми примерами и заданиями - это ускоренный путь вместо самостоятельного изучения документации
- Tool Calling (Function Calling) - ключевой механизм: агент получает задачу, Gemini выбирает нужный инструмент, выполняет его, и обрабатывает результат в цикле
- Agenticity возникает когда агент может автономно принимать решения о вызове нескольких функций в последовательности без вмешательства человека
- Vertex AI предлагает интеграцию со множеством Google сервисов (Cloud Storage, BigQuery, Cloud SQL) что упрощает подключение инструментов
- Python SDK (google-generativeai или google-cloud-vertexai) позволяет быстро прототипировать агентов локально перед развертыванием
- Курс включает практические проекты - не просто теория, но создание работающих агентов для реальных бизнес-сценариев
- Gemini моделям не требуется fine-tuning для базовых агентов - они работают с in-context learning и tool calling из коробки
- Развертывание на Vertex AI обеспечивает автоматическое масштабирование, логирование и мониторинг без управления инфраструктурой
- Cost-effective: pay-per-token модель Gemini API дешевле чем GPT-4, особенно для долгих цепочек reasoning
- Интеграция с Cloud Functions позволяет использовать агентов как backend для мобильных приложений и веб-сервисов через HTTP endpoints

## Подводные камни
_Не упомянуты_
