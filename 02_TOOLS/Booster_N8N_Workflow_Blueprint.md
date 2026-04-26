# 📐 Чертеж воркфлоу n8n: AI-Sales Booster

## Источники данных (Triggers):
- UIS / MTS Exolve API: Звонки.
- Wazzup API: WhatsApp и Telegram.
- Внутренний канал: MAX.

## Шаги воркфлоу:
1. Trigger (Webhook): Прием данных.
2. Function Node: Нормализация телефона.
3. HTTP Request (Whisper): Транскрибация аудио.
4. AI Agent (Claude 3.5): Анализ и JSON.
5. CRM Connector: Поиск контакта.
6. Switch (Update/Create): Обновление или создание.
7. Telegram Bot: Уведомление Максиму.