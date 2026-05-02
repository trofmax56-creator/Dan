---
title: Claude Code Routines + cron — ночной агент для Bitrix24 и МойСклад без участия менеджера
tags: #biz_recipe #automation #bitrix24 #moysklad #claude_code #cron #action_needed
---

### 1. Описание идеи
Claude Code Routines запускает агента по расписанию, но имеет лимиты на частоту и не поддерживает передачу сложных инструкций. Решение: cron на VPS запускает `claude --print` с инструкцией из markdown-файла. Агент ночью обходит просроченные задачи в Bitrix24, актуализирует остатки в МойСклад, формирует утренний отчёт — всё без участия менеджера.

### 2. Технический стек
- AI: Claude Code (claude-sonnet-4-6)
- CRM/ERP: Bitrix24 (REST API), МойСклад (REST API)
- Middleware: cron (Linux), bash-скрипт, Telegram Bot API (для доставки отчёта)

### 3. Пошаговый план внедрения
1. Создать директорию `/home/agent/routines/` с файлами инструкций: `morning_report.md`, `overdue_tasks.md`, `stock_check.md`
2. Написать bash-обёртку `run_routine.sh` (код ниже)
3. Добавить задания в crontab:
   ```
   0 7  * * 1-5  /home/agent/routines/run_routine.sh morning_report
   0 22 * * 1-5  /home/agent/routines/run_routine.sh overdue_tasks
   0 6  * * *    /home/agent/routines/run_routine.sh stock_check
   ```
4. Каждый markdown-файл содержит системный промпт для агента + конкретную задачу
5. Результат claude → отправить в Telegram через curl или python-telegram-bot

### 4. Промпты и Код
```bash
#!/bin/bash
# /home/agent/routines/run_routine.sh

ROUTINE=$1
INSTRUCTION_FILE="/home/agent/routines/${ROUTINE}.md"
LOG_FILE="/home/agent/logs/${ROUTINE}_$(date +%Y%m%d).log"
BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
CHAT_ID="${TELEGRAM_CHAT_ID}"

if [ ! -f "$INSTRUCTION_FILE" ]; then
  echo "Routine not found: $ROUTINE" && exit 1
fi

PROMPT=$(cat "$INSTRUCTION_FILE")

RESULT=$(claude --print -p "$PROMPT" 2>&1)
echo "$RESULT" > "$LOG_FILE"

# Отправка в Telegram
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  -d "text=🤖 ${ROUTINE}:%0A${RESULT:0:3800}" \
  -d "parse_mode=Markdown"
```

```markdown
<!-- /home/agent/routines/morning_report.md -->
Подключись к MCP bitrix24 и moysklad.

Задача: Сформируй утренний отчёт для руководителя.

1. Из Bitrix24: получи список задач со статусом "просрочено" за вчера (метод tasks.task.list, filter DEADLINE < сегодня, STATUS != 5)
2. Из МойСклад: получи товары с остатком < 5 единиц (entity/stock, filter stock < 5)
3. Верни отчёт в формате:

**Утренний отчёт [дата]**
📌 Просроченных задач: N
- [имя задачи] — ответственный
...
📦 Критически низкий остаток: N позиций
- [товар] — остаток X шт.
```

```markdown
<!-- /home/agent/routines/overdue_tasks.md -->
Подключись к MCP bitrix24.

Задача: Вечерний обход просроченных задач.

1. Получи все задачи со сроком сегодня и статусом не завершено
2. Для каждой задачи — добавь комментарий: "⏰ Напоминание: задача не завершена в срок. Обновите статус."
   (метод: tasks.task.commentItem.add)
3. Верни список задач, которым добавлен комментарий
```

### 5. Оценка эффективности
- Сложность: 3/5
- ROI: исключает ручной мониторинг задач и остатков; руководитель получает утренний отчёт до начала рабочего дня; экономия 30–45 мин/день

**Ссылки:** [[02_TOOLS/MoySklad_API]] | [[02_TOOLS/Bitrix24_API]] | [[05_BIZ_RECIPES/058_claude_code_vps_telegram_crm_agent]]
