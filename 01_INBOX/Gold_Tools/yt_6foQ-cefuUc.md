---
source: YouTube / Level Up with Louis
date: 2026-05-01
original: https://youtube.com/watch?v=6foQ-cefuUc
category: GOLD_TOOLS
tags: [Cursor AI, Azure, API Integration, Azure OpenAI, IDE Configuration, Authentication, Cloud Services, Developer Tools, Setup Guide, 2026]
extracted_by: Claude Haiku
---

## Суть
Настройка подключения Azure API к Cursor AI для использования Microsoft Azure сервисов в кодовой среде разработчика.

## Бизнес-сценарий
Разработчики, использующие Cursor IDE, которые хотят интегрировать Azure API ключи для подключения облачных сервисов Microsoft Azure к среде разработки и автоматизации кодовых операций.

## Алгоритм реализации
1. Шаг 1: Открыть Cursor IDE и перейти в раздел Settings (Настройки) через меню File → Preferences → Settings или используя сочетание Ctrl+,
2. Шаг 2: В строке поиска Settings найти 'Azure' или перейти в раздел 'API Keys' / 'Cloud Integration'
3. Шаг 3: Получить Azure API ключ из Azure Portal (portal.azure.com) — зайти в Resource Groups → выбрать нужный ресурс → скопировать API Key или Connection String
4. Шаг 4: В окне настроек Cursor вставить Azure API ключ в соответствующее поле (обычно в поле 'Azure API Key' или 'API Key')
5. Шаг 5: Выбрать тип сервиса Azure, который требуется подключить (например, Azure OpenAI, Cognitive Services, Storage Account и т.д.)
6. Шаг 6: Сохранить настройки (нажать 'Save' или 'Apply') и проверить соединение кнопкой 'Test Connection'
7. Шаг 7: Перезагрузить Cursor IDE для применения изменений
8. Шаг 8: Использовать Azure сервисы в коде или через встроенные функции Cursor с использованием установленного подключения

## Технический стек
- Cursor AI IDE
- Microsoft Azure
- Azure Portal
- Azure API Keys
- Azure Cognitive Services (опционально)
- Azure OpenAI Service (опционально)
- Azure Storage Account (опционально)
- REST API
- OAuth 2.0 (для некоторых сервисов)

## Связки инструментов
- Cursor IDE Settings → Azure API Configuration
- Azure Portal → Resource Groups → API Keys/Connection String
- Azure API → Cursor IDE Request Handler
- Cursor Configuration File → env variables

## Конфигурация и параметры
- Cursor IDE — версия 0.42+ (2026 Guide указывает на актуальную версию)
- Меню Settings: File → Preferences → Settings или Ctrl+, (Windows/Linux) / Cmd+, (Mac)
- Раздел поиска Settings: введите 'Azure' для быстрого поиска
- Поле ввода 'Azure API Key': вставить полный API ключ из Azure Portal (формат обычно 32+ символов)
- Поле 'API Endpoint': URL эндпоинта Azure сервиса (например, https://[resource-name].openai.azure.com/)
- Поле 'Deployment Name': название развёрнутого ресурса в Azure (если используется Azure OpenAI)
- Поле 'API Version': версия API, которую использует Azure сервис (например, 2024-02-15 для Azure OpenAI)
- Кнопка 'Test Connection': проверяет валидность ключа и соединение
- Опция 'Save credentials': сохранять ли учётные данные в локальный конфиг Cursor (рекомендуется отключить для безопасности)

## Ключевые инсайты
- Azure API ключи чувствительны к регистру и не должны содержать пробелов — копируйте ровно из Azure Portal без дополнительных символов
- Cursor использует локальное хранилище для API ключей, шифруя их в операционной системе — не хранит на серверах
- При использовании Azure OpenAI необходимо указать не только API ключ, но и Deployment Name, иначе запросы вернут 404 ошибку
- Версия API важна: разные версии Azure OpenAI имеют разный формат параметров — используйте версию совместимую с вашим кодом
- Эндпоинт Azure отличается от обычного OpenAI — формат: https://[your-resource-name].openai.azure.com/ (на конце слэш обязателен)
- Если ключ не работает, проверьте в Azure Portal, что у него есть нужные permissions и срок действия не истёк
- Cursor кэширует соединение — после смены ключа может потребоваться перезагрузка IDE или очистка кэша
- Для максимальной безопасности используйте переменные окружения вместо прямого ввода ключа в Settings (установите AZURE_API_KEY в .env)

## Подводные камни
- Типичная ошибка: забыть слэш в конце эндпоинта (https://resource.openai.azure.com) — это вызовет ошибки маршрутизации API
- Если ключ содержит спецсимволы, Cursor может неправильно их интерпретировать — используйте кавычки при вставке в конфиг-файл
- Azure API версии быстро обновляются — старая версия API в Settings может привести к несовместимости с новыми методами Azure
- Соединение не тестируется автоматически при запуске — нужно явно нажать 'Test Connection' для проверки перед использованием
- Если Cursor установлен в режиме portable или в папке только для чтения, он не сможет сохранить ключ в локальное хранилище
- Некоторые корпоративные Azure подписки требуют дополнительной аутентификации через Azure CLI (az login) перед использованием ключей
