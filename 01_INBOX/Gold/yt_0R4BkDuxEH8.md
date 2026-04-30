---
source: YouTube / Игорь Зуевич
date: 2026-01-17
original: https://youtube.com/watch?v=0R4BkDuxEH8
category: GOLD
tags: []
extracted_by: Claude Haiku
status: archive
reason: low_score
score: Pain=5 Dev=8 Profit=4 ИТОГ=17
---

## Суть
Обзор 25 критических нод n8n, которые являются основой для построения 99% всех автоматизаций и AI-агентов. Видео показывает базовый набор нод, необходимых для создания рабочих flows без необходимости использования сложных интеграций.

## Бизнес-сценарий
Для разработчиков, владельцев бизнеса и автоматизаторов, которые создают workflows в n8n. Задача: получить полный справочник основных нод для быстрого построения автоматизаций без глубокого изучения всего функционала платформы.

## Алгоритм реализации
1. Шаг 1: Понимание основных категорий нод (триггеры, обработка данных, условия, интеграции)
2. Шаг 2: Изучение нод работы с данными (Split, Merge, Transform, Code execution)
3. Шаг 3: Изучение условных нод (Switch, If-Then-Else логика)
4. Шаг 4: Изучение нод интеграции (HTTP Request, API calls, webhooks)
5. Шаг 5: Изучение нод для работы с AI (OpenAI, ChatGPT, Claude интеграции)
6. Шаг 6: Построение простого workflow с комбинацией изученных нод
7. Шаг 7: Тестирование и отладка workflow через встроенный дебаггер n8n

## Технический стек
- n8n - платформа для автоматизации
- Webhook - для входящих событий
- HTTP Request node - для API интеграций
- Code node - для JavaScript/Python кода
- Function node - для преобразования данных
- Switch node - для условной логики
- Merge node - для объединения данных
- Split In Batches - для обработки массивов
- OpenAI API - для AI функций
- ChatGPT API - для использования ChatGPT
- Claude API - для использования Claude
- Set node - для установки переменных
- Rename node - для переименования полей
- Aggregator node - для группировки данных

## Связки инструментов
- Webhook триггер → HTTP Request → Code node → AI API (OpenAI/Claude) → Set node → вывод результата
- Database trigger → Function node → Switch (условие) → Split In Batches → параллельная обработка → Merge → финальный вывод
- Form submission → Rename node → Transform data → HTTP POST → Email notification
- API call → Parse JSON → Function node → Store in database → Webhook response

## Конфигурация и параметры
- Webhook node: выбрать метод (GET/POST), установить аутентификацию, включить 'Return binary response' если нужны файлы
- HTTP Request node: указать URL, метод (GET/POST/PUT/DELETE), в Headers добавить Authorization если требуется
- Code node: выбрать язык (JavaScript по умолчанию), пользовать переменные через $node[имя_ноды].data или items
- Function node: похож на Code но упрощённый, используется для простых преобразований
- Switch node: добавить условия (if-else), для каждого условия указать поле и значение для проверки
- Set node: добавить новые переменные через JSON interface или Simple interface, каждое новое поле вводится вручную
- Split In Batches: установить 'Batch Size' (количество элементов в одной порции), 'Interval' (задержка между порциями в мс)
- OpenAI node: вставить API key, выбрать модель (gpt-4, gpt-3.5-turbo), составить промпт
- ChatGPT node: подключить через OpenAI API key, выбрать параметры (temperature, max tokens)
- Merge node: выбрать режим (combine first, combine by key, combine all), указать поле для объединения если нужна группировка

## Ключевые инсайты
- Webhook node - самая используемая точка входа для запуска workflows. Каждый webhook имеет уникальный URL который можно интегрировать в другие системы
- HTTP Request node может заменить 99% встроенных интеграций в n8n, если вы знаете нужный API и можете составить правильный запрос
- Code node позволяет писать JavaScript прямо в workflow без необходимости отдельного backend сервера
- Switch node - ключевой элемент для условной логики. Одно условие может привести к разным веткам workflow
- Split In Batches позволяет обрабатывать большие массивы данных без риска перегрузки, разбивая на порции
- Set node используется для создания промежуточных переменных которые понадобятся позже в workflow
- AI nodes (OpenAI, ChatGPT, Claude) - это новый уровень автоматизации, позволяющий добавить интеллект в process
- Merge node критичен при использовании Split In Batches - необходимо объединить результаты обратно
- Function node быстрее чем Code node для простых задач, используйте если не нужна полная мощь JavaScript
- Rename node упрощает преобразование структуры данных, особенно полезен когда API возвращает поля с неудачными именами

## Подводные камни
_Не упомянуты_
