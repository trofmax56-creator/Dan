---
title: Claude Code + МойСклад — авто-документирование бизнес-процессов через MCP
tags: #biz_recipe #automation #moysklad #claude_code #action_needed
---

### 1. Описание идеи
Claude Code подключается к МойСклад через MCP-сервер и автоматически создаёт/обновляет документацию бизнес-процессов: схемы складских операций, описания типов товаров, регламенты. Параллельно — авто-коммит изменений через Git, история всегда актуальна.

### 2. Технический стек
- AI: Claude Code (claude-sonnet-4-6)
- CRM/ERP: МойСклад (REST API)
- Middleware: MCP server (Node.js), GitHub Desktop / git CLI

### 3. Пошаговый план внедрения
1. Создать MCP-сервер для МойСклад (см. код ниже) — эндпоинты: `get_products`, `get_orders`, `get_warehouses`
2. Прописать сервер в `claude --print-config` → раздел `mcpServers`
3. Создать файл `CLAUDE.md` с инструкцией: "При запуске сессии — загрузи данные из МойСклад и обнови документацию в папке `03_GUIDES/moysklad/`"
4. Запускать `claude` из корня репозитория; он сам подтянет данные и обновит `.md`-файлы
5. Настроить git hook `post-session`: `git add . && git commit -m "auto-doc update $(date)"`

### 4. Промпты и Код
```json
// ~/.claude/settings.json — регистрация MCP-сервера
{
  "mcpServers": {
    "moysklad": {
      "command": "node",
      "args": ["/path/to/moysklad-mcp/index.js"],
      "env": {
        "MOYSKLAD_TOKEN": "YOUR_TOKEN_HERE"
      }
    }
  }
}
```

```js
// moysklad-mcp/index.js — минимальный MCP-сервер
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "moysklad", version: "1.0.0" }, {
  capabilities: { tools: {} }
});

server.setRequestHandler("tools/list", async () => ({
  tools: [{ name: "get_products", description: "Список товаров МойСклад", inputSchema: { type: "object", properties: {} } }]
}));

server.setRequestHandler("tools/call", async (req) => {
  if (req.params.name === "get_products") {
    const res = await fetch("https://api.moysklad.ru/api/remap/1.2/entity/product?limit=50", {
      headers: { Authorization: `Bearer ${process.env.MOYSKLAD_TOKEN}` }
    });
    const data = await res.json();
    return { content: [{ type: "text", text: JSON.stringify(data.rows.map(p => ({ id: p.id, name: p.name, code: p.code }))) }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

```
SYSTEM (в CLAUDE.md):
Подключись к MCP-серверу moysklad. Получи список товаров и складов.
Обнови файл 03_GUIDES/moysklad/product_catalog.md в формате markdown-таблицы.
Если файл не существует — создай его. Зафиксируй изменения через git.
```

### 5. Оценка эффективности
- Сложность: 4/5
- ROI: устраняет ручное ведение документации; экономия 2–4 ч/нед у администратора склада
