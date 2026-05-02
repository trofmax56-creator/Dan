---
source: YouTube / Microsoft Reactor
date: 2026-04-29
original: https://youtube.com/watch?v=mFZHq5mTt0A
category: GOLD_CRM
tags: []
extracted_by: Claude Haiku
---

## Суть
Развертывание AI-агентов на базе LangChain и LangGraph на платформе Microsoft Foundry для создания масштабируемых и управляемых автоматизированных систем обработки данных и взаимодействия с внешними сервисами.

## Бизнес-сценарий
Разработчики и DevOps-инженеры используют Microsoft Foundry для хостирования агентов на основе LangChain/LangGraph, которые автоматизируют сложные многошаговые процессы обработки данных, взаимодействуют с внешними API, управляют рабочими процессами и принимают решения на основе контекста.

## Алгоритм реализации
1. 1. Инициализация проекта LangChain/LangGraph локально с установкой зависимостей (langchain, langgraph, python-dotenv)
2. 2. Определение структуры агента: создание узлов графа, функций инструментов и логики переходов между состояниями
3. 3. Реализация интеграции с внешними API и сервисами (веб-поиск, получение данных, взаимодействие с БД)
4. 4. Локальное тестирование агента с использованием pytest или встроенных утилит отладки LangGraph
5. 5. Подготовка конфигурации для развертывания: определение переменных окружения, настройка логирования и мониторинга
6. 6. Разработка API-слоя для взаимодействия с агентом (FastAPI или Flask с маршрутами /invoke, /stream)
7. 7. Создание Docker-контейнера с указанием base image (python:3.11+), установкой зависимостей, копированием кода
8. 8. Настройка конфигурации Foundry: определение endpoint URL, аутентификационных токенов, ресурсов (CPU, память)
9. 9. Развертывание образа на Microsoft Foundry через CLI или веб-интерфейс платформы
10. 10. Мониторинг и логирование работы агента с использованием встроенных инструментов Foundry для отслеживания состояния, ошибок и производительности

## Технический стек
- LangChain (core, agents, tools)
- LangGraph (state graphs, node definitions, edges)
- Python 3.10+
- FastAPI или Flask (для API-слоя)
- Docker и Docker Compose
- Microsoft Foundry
- OpenAI API (или другой LLM)
- Requests или httpx (для HTTP-запросов)
- Python-dotenv (управление переменными окружения)
- Logging модуль Python
- Pytest (тестирование)
- SQLAlchemy или другой ORM для работы с БД (если требуется)

## Связки инструментов
- LangChain инициализация → определение состояния графа → создание узлов и инструментов → настройка переходов → compile()
- API endpoint → receive user input → invoke agent/stream → return response → log results
- Local development → Docker build → Docker push to registry → Foundry deploy → health checks → monitoring
- Environment variables (API keys) → injected at runtime → passed to LLM/tools → secure credential management

## Конфигурация и параметры
- Определение StateGraph с типом состояния (TypedDict или BaseModel с полями: messages, user_input, context)
- Создание узлов графа через @graph.add_node('node_name', callable_function)
- Регистрация инструментов через tools = [...] и bind_tools() для привязки к LLM
- Настройка переходов: graph.add_edge('node_a', 'node_b') или условные переходы через graph.add_conditional_edges()
- Компиляция графа: compiled_graph = graph.compile()
- FastAPI маршруты: POST /invoke с телом {query, session_id}, GET /status/{agent_id}
- Docker Dockerfile: FROM python:3.11-slim, WORKDIR /app, COPY requirements.txt, RUN pip install -r requirements.txt, COPY . ., CMD ['uvicorn', 'main:app', '--host', '0.0.0.0']
- Foundry конфигурация: deployment.yaml с указанием container image, resource limits (requests/limits для CPU и памяти), environment variables, port exposure
- Переменные окружения: OPENAI_API_KEY, FOUNDRY_API_KEY, LOG_LEVEL, DB_CONNECTION_STRING
- Health check endpoint: GET /health возвращает {status: 'healthy', uptime_seconds, agent_version}

## Ключевые инсайты
- LangGraph компилируется в неизменяемый граф перед развертыванием, что обеспечивает консистентность поведения во всех инстансах
- Использование state machine подхода позволяет легко отслеживать прогресс выполнения агента и восстанавливаться после сбоев на конкретном узле
- Streaming ответов через SSE или WebSocket уменьшает время восприятия (time-to-first-token) и улучшает UX для пользователей
- Docker контейнеризация гарантирует, что агент работает идентично на локальной машине, в CI/CD и на Foundry без проблем 'работает на моей машине'
- Микросервисная архитектура с отделением API слоя от логики агента позволяет масштабировать и обновлять компоненты независимо
- Мониторинг через структурированное логирование (JSON logs с trace_id) критичен для отладки проблем в production
- Кэширование ответов LLM и результатов инструментов значительно снижает затраты на API токены и время отклика
- Graceful shutdown с завершением текущих запросов (timeout 30 сек) предотвращает потерю данных при обновлениях

## Подводные камни
- LangGraph требует явной компиляции (graph.compile()) перед использованием — код без компиляции вызовет ошибку на runtime
- При использовании инструментов обязательно указывать type hints для каждого параметра, иначе LLM не сможет корректно вызвать функцию
- Переменные окружения в Docker контейнере должны быть переданы при запуске (docker run -e KEY=value), иначе агент упадет при попытке использовать None API ключ
- Microsoft Foundry требует корректного форматирования logs в stdout/stderr (не файлы) — стандартное логирование Python может быть невидимо
- При потоковой передаче (streaming) ответа нельзя отправлять большие объемы за раз — буферизировать в chunks для долгих выполнений
- Session/conversation state должна быть явно управляема и сохраняться между вызовами — в stateless контейнере контекст будет потерян после запроса
- Timeout на внешние API вызовы обязателен (requests timeout=10), иначе зависший API может заморозить весь контейнер
- Версионирование Docker образа критично — используйте теги вида v1.2.3, а не latest, для контролируемого rollback при проблемах
