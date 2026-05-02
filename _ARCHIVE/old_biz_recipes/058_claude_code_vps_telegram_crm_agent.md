---
title: Claude Code на VPS + Telegram-мост — CRM/ERP агент без браузера и VPN
tags: #biz_recipe #automation #bitrix24 #moysklad #claude_code #telegram #action_needed
---

### 1. Описание идеи
Claude Code разворачивается на VPS (любой DigitalOcean/Hetzner), получает доступ к Bitrix24 и МойСклад через MCP-серверы. Управление — только через Telegram: менеджер пишет задачу боту, агент выполняет и возвращает результат. Не нужен VPN, браузер или локальная подписка. Один агент на команду.

### 2. Технический стек
- AI: Claude Code (claude-sonnet-4-6 / opus-4-7)
- CRM/ERP: Bitrix24 REST API, МойСклад REST API
- Middleware: Telegram Bot API, n8n (как Telegram-мост), VPS (Ubuntu 22.04)

### 3. Пошаговый план внедрения
1. Арендовать VPS (минимум 2 CPU, 4 GB RAM) → установить Node.js 20+, Python 3.11+, Claude Code CLI
2. Создать Telegram-бота через @BotFather → получить `BOT_TOKEN`
3. Настроить n8n на VPS: Webhook-триггер на входящие сообщения бота
4. n8n → SSH Execute node (или HTTP Request к локальному API) → запускает `claude --print -p "{{message}}"` в нужной директории проекта
5. Ответ Claude → n8n → `sendMessage` в Telegram обратно пользователю
6. В `~/.claude/settings.json` на VPS подключить MCP-серверы Bitrix24 и МойСклад
7. В `CLAUDE.md` проекта описать: какие данные брать из Bitrix24, какие из МойСклад, формат ответов

### 4. Промпты и Код
```bash
# Установка Claude Code на VPS
npm install -g @anthropic-ai/claude-code
export ANTHROPIC_API_KEY="sk-ant-..."
claude --version  # проверка
```

```python
# Минимальный Telegram-мост (без n8n, на Python)
import os, subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

ALLOWED_IDS = {123456789}  # Telegram ID разрешённых пользователей

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_IDS:
        return
    user_msg = update.message.text
    result = subprocess.run(
        ["claude", "--print", "-p", user_msg],
        capture_output=True, text=True, cwd="/home/agent/crm-project"
    )
    await update.message.reply_text(result.stdout[:4000] or result.stderr[:4000])

app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
```

```json
// ~/.claude/settings.json на VPS
{
  "mcpServers": {
    "bitrix24": {
      "command": "node",
      "args": ["/home/agent/mcp-bitrix/index.js"],
      "env": { "BITRIX_WEBHOOK": "https://your.bitrix24.ru/rest/1/TOKEN/" }
    },
    "moysklad": {
      "command": "node",
      "args": ["/home/agent/mcp-moysklad/index.js"],
      "env": { "MOYSKLAD_TOKEN": "YOUR_TOKEN" }
    }
  }
}
```

```
# CLAUDE.md (в /home/agent/crm-project/)
Ты — CRM-агент компании. Отвечай только на вопросы по задачам, сделкам и складу.
- Для данных по сделкам и лидам → используй MCP bitrix24
- Для данных по товарам и остаткам → используй MCP moysklad
- Формат ответа: краткий, без markdown, одним сообщением
- Язык: русский
```

### 5. Оценка эффективности
- Сложность: 4/5
- ROI: один агент заменяет ручной поиск данных в двух системах; экономия 1–2 ч/день менеджера; не нужен VPN для работы с Claude

**Ссылки:** [[02_TOOLS/MoySklad_API]] | [[02_TOOLS/Bitrix24_API]] | [[03_GUIDES/claude_code_mcp_setup]]
