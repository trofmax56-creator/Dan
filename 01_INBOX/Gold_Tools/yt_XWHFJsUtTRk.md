---
source: YouTube / Yash Jain
date: 2026-04-30
original: https://youtube.com/watch?v=XWHFJsUtTRk
category: GOLD_TOOLS
tags: [LangGraph, multi-agent, AI-агент, supervisor, worker-delegation, LangChain, Claude, workflow, automation, Python, StateGraph, tool-use, routing, distributed-processing]
extracted_by: Claude Haiku
---

## Суть
Автоматизация распределения задач между несколькими AI-агентами через архитектуру Supervisor-Workers в LangGraph. Супервизор анализирует входящие запросы и делегирует их специализированным рабочим агентам для параллельной обработки, что ускоряет выполнение сложных многошаговых задач.

## Бизнес-сценарий
Компании, использующие LangGraph, создают многоагентные системы для автоматизации сложных бизнес-процессов: обработка клиентских запросов, анализ данных, генерация отчётов. Супервизор распределяет работу между специализированными агентами (поиск информации, анализ, написание), оптимизируя время обработки и качество результатов.

## Алгоритм реализации
1. 1. Инициализация LangGraph проекта и импорт необходимых модулей (StateGraph, MessageState, tool_node)
2. 2. Определение состояния системы — MessageState с полями для хранения сообщений и истории диалога
3. 3. Создание рабочих агентов (Workers) — каждый агент получает свой набор инструментов и системный prompt, определяющий специализацию
4. 4. Реализация Supervisor ноды — анализирует запрос и определяет какой Worker должен его обработать или завершает работу
5. 5. Построение графа переходов — связывание Supervisor и Worker нод с условной логикой маршрутизации
6. 6. Определение входной точки (entry_point) и точек завершения (end_states)
7. 7. Компиляция графа в исполняемый workflow с помощью graph.compile()
8. 8. Запуск системы через invoke() с входящим сообщением пользователя
9. 9. Обработка ответов и логирование результатов каждого агента

## Технический стек
- LangGraph (основной фреймворк для построения графа agentов)
- LangChain (интеграция с LLM и инструментами)
- Claude API или другой LLM (для работы супервизора и workers)
- Python (язык реализации)
- StateGraph (класс для определения структуры графа)
- MessageState (состояние диалога)
- tool_node (для оборачивания инструментов)
- Pydantic (для типизации данных)
- JSON (для структурирования инструкций и ответов)

## Связки инструментов
- User Input → Supervisor Node (LangGraph) → Router Logic → Worker Nodes (LLM + Tools) → Tool Execution → Response Aggregation → Final Output
- Supervisor (Claude API) → analyzes request → decides which Worker → Worker (Claude API with tools) → executes task → returns to Supervisor → aggregates results

## Конфигурация и параметры
- StateGraph определение: class MultiAgentState(TypedDict): messages: list[BaseMessage]
- Supervisor system prompt: определяет список доступных Workers и критерии выбора агента
- Worker system prompt: специализированные инструкции для каждого агента (например, 'Research Agent', 'Writing Agent', 'Analysis Agent')
- Tool definition: функции-инструменты для каждого Workers (web_search, file_read, data_analysis и т.д.)
- Router outputs: должен возвращать одно из значений ['research_worker', 'writing_worker', 'analysis_worker', '__end__']
- Conditional edge: использует условие для маршрутизации на основе output Supervisor ноды
- Message format: все сообщения следуют формату LangChain Message (role + content)
- Timeout settings: опциональная настройка максимального времени выполнения агента

## Ключевые инсайты
- Supervisor должен быть более 'простым' LLM чем Workers — это снижает затраты на токены при маршрутизации запросов
- Использование structured output (JSON с полем 'next') для надёжной маршрутизации вместо парсинга текста
- Каждый Worker должен иметь чётко определённый scope инструментов — это предотвращает дублирование и конфликты
- Параллельная работа Workers невозможна в стандартном LangGraph — используется последовательная делегация, но результаты накапливаются в StateGraph
- Для避免 бесконечных циклов используется явное условие завершения (__end__) в Router логике
- Tool-use нода должна оборачивать результаты инструментов в правильный формат Message для StateGraph
- Состояние (State) хранит историю всех сообщений — это позволяет каждому Workers видеть контекст предыдущих действий
- Ошибки в инструментах (HTTP ошибки, timeouts) должны быть обработаны и переданы в State как сообщения об ошибках для Supervisor

## Подводные камни
- Если Router вернёт несуществующее имя Worker — граф упадёт. Необходимо валидировать output на уровне LLM через system prompt
- LangGraph не распараллеливает Workers автоматически — это последовательная система. Для параллелизма нужно использовать asyncio вручную
- Message history может стать очень большой и исчерпать контекстное окно LLM — используйте summarization или sliding window
- Tool errors не должны прерывать поток — их нужно ловить в try-except и передавать как текстовые сообщения в граф
- Если Worker заходит в бесконечный loop (например, повторяет один и тот же tool) — граф зависнет. Добавьте max_iterations ограничение
- State не автоматически очищается между запусками — убедитесь что State инициализируется свежим для каждого нового invoke()
- LLM может 'забыть' о доступных Workers если system prompt слишком длинный — держите Supervisor prompt компактным
