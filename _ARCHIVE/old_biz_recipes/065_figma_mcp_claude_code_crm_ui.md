---
title: Figma Context MCP — Claude Code читает Figma и генерирует CRM-интерфейсы
tags: #biz_recipe #automation #bitrix24 #figma #mcp #claude_code #ui #action_needed
source: edvardgrishin27/168 (Figma Context MCP)
date: 2026-04-23
---

### 1. Описание идеи

Figma Context MCP (https://github.com/GLips/Figma-Context-MCP) позволяет Claude Code напрямую читать компоненты из Figma через MCP-сервер: получать структуру фреймов, стили, цвета, шрифты, размеры. Применение для CRM: дизайнер рисует макет кастомного модуля в Figma → Claude Code читает его через MCP и генерирует готовый HTML/CSS/React-компонент для Bitrix24 или кастомного портала. Передача макета разработчику через текст больше не нужна.

### 2. Технический стек

- MCP: Figma Context MCP (Node.js) — https://github.com/GLips/Figma-Context-MCP
- AI: Claude Code (claude-sonnet-4-6 / claude-opus-4-7)
- CRM: Bitrix24 (кастомные компоненты в открытых линиях / REST API)
- Frontend: React / Vue / чистый HTML+CSS
- Figma API Token: из настроек аккаунта Figma

### 3. Пошаговый план внедрения

**Шаг 1 — Установка Figma Context MCP**
```bash
# Клонировать и установить
git clone https://github.com/GLips/Figma-Context-MCP
cd Figma-Context-MCP
npm install && npm run build

# Получить Figma Personal Access Token:
# Figma → Settings → Security → Personal access tokens → Create new token
```

**Шаг 2 — Подключить к Claude Code**
```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "figma": {
      "command": "node",
      "args": ["/path/to/Figma-Context-MCP/dist/index.js"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "figd_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

**Шаг 3 — Подготовка Figma-файла**
Структура фрейма для CRM-компонента:
```
CRM Components/
  ├── LeadCard/          ← карточка лида
  │   ├── Header
  │   ├── ContactInfo
  │   └── Actions
  ├── DealStageBar/      ← прогресс-бар воронки
  └── TaskWidget/        ← виджет задач
```
Называть слои понятно — Claude читает имена как описание.

**Шаг 4 — Промпт для генерации компонента**
```
Используй Figma MCP для чтения фрейма "LeadCard" из файла [FIGMA_URL].

После прочтения:
1. Опиши структуру компонента (слои, размеры, цвета, шрифты)
2. Сгенерируй React-компонент с TypeScript
3. CSS — inline-styles или CSS Modules (без Tailwind)
4. Props: { lead_name, company, phone, status, manager }
5. Цвета и шрифты — строго из Figma, не придумывай
6. Компонент должен работать в Bitrix24 Open Channel UI
```

**Шаг 5 — Пример результата**
```tsx
// LeadCard.tsx — сгенерировано Claude Code из Figma
import React from 'react';

interface LeadCardProps {
  lead_name:  string;
  company:    string;
  phone:      string;
  status:     'new' | 'in_progress' | 'closed';
  manager:    string;
}

const STATUS_COLORS = {
  new:         '#2563EB',
  in_progress: '#D97706',
  closed:      '#16A34A',
};

export const LeadCard: React.FC<LeadCardProps> = ({
  lead_name, company, phone, status, manager
}) => (
  <div style={{
    background: '#FFFFFF',
    borderRadius: 12,
    padding: '16px 20px',
    boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
    fontFamily: 'Inter, sans-serif',
    width: 320,
  }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
      <span style={{ fontWeight: 600, fontSize: 15, color: '#111827' }}>{lead_name}</span>
      <span style={{
        background: STATUS_COLORS[status],
        color: '#fff',
        borderRadius: 6,
        padding: '2px 8px',
        fontSize: 11,
        fontWeight: 500,
      }}>
        {status === 'new' ? 'Новый' : status === 'in_progress' ? 'В работе' : 'Закрыт'}
      </span>
    </div>
    <div style={{ color: '#6B7280', fontSize: 13, marginBottom: 4 }}>{company}</div>
    <div style={{ color: '#374151', fontSize: 13 }}>{phone}</div>
    <div style={{ marginTop: 12, fontSize: 12, color: '#9CA3AF' }}>Менеджер: {manager}</div>
  </div>
);
```

**Шаг 6 — Интеграция в Bitrix24**
```javascript
// Встраивание кастомного компонента в Bitrix24 через BX.ready
BX.ready(() => {
  const container = document.getElementById('crm-lead-widget');
  if (!container) return;

  // Получаем данные лида через REST API
  BX24.callMethod('crm.lead.get', { id: LEAD_ID }, (result) => {
    const lead = result.data();
    ReactDOM.render(
      React.createElement(LeadCard, {
        lead_name: lead.NAME,
        company:   lead.COMPANY_TITLE,
        phone:     lead.PHONE?.[0]?.VALUE || '',
        status:    lead.STATUS_ID === 'NEW' ? 'new' : 'in_progress',
        manager:   lead.ASSIGNED_BY_NAME,
      }),
      container
    );
  });
});
```

### 4. Сценарии использования в CRM

| Задача | Figma фрейм | Выход Claude Code |
|--------|-------------|-------------------|
| Карточка лида | LeadCard | React-компонент |
| Воронка продаж | DealPipeline | Интерактивный Kanban |
| Дашборд менеджера | ManagerDashboard | HTML-виджет |
| Шаблон КП | ProposalTemplate | HTML-документ для PDF |
| Чат-виджет | ChatWidget | Встраиваемый iframe |

### 5. Нюансы

- Figma Context MCP читает только публичные файлы или файлы, доступные токену. Для командного использования создать отдельный Figma-аккаунт сервиса
- Сложные анимации (Auto Layout, Smart Animate) Claude не воспроизводит — только статичная вёрстка
- Именование слоёв в Figma критично: `Button/Primary` → Claude понимает как primary button, `Frame 123` → Claude угадывает назначение
- Figma Context MCP возвращает JSON с деревом компонентов — при большом файле контекст раздувается. Передавать конкретный фрейм, не весь файл

### 6. Оценка эффективности

- Сложность: 3/5
- ROI: передача макета разработчику через текстовое описание занимает 2–4 часа; Claude Code читает Figma за 30 секунд и пишет компонент за 2–5 минут; экономия на каждом компоненте — 1–3 часа разработки

**Ссылки:** [[02_TOOLS/Figma_MCP]] | [[02_TOOLS/Bitrix24_API]] | [[03_GUIDES/claude_code_mcp_setup]]
