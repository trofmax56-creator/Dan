---
title: План чистки репозитория Dan
date: 2026-04-30
author: Claude + Максим
status: в работе
---

# 🧹 План чистки репозитория

---

## 🗑️ УДАЛИТЬ (однозначно, без раздумий)

- [ ] `02_TOOLS/021.md` — пустая заглушка
- [ ] `03_GUIDES/031.md` — пустая заглушка
- [ ] `04_PROJECTS/041.md` — пустая заглушка
- [ ] `TEMPLATES/T1.md` — пустой шаблон без содержания
- [ ] `02_TOOLS/Scripts/yt_discovery_report.md` — старый отчёт v1.0, заменён `infra_digest_*`
- [ ] `02_TOOLS/Scripts/dan_discovery.session` — дубль сессии, рабочая в корне (`dan_session`)
- [ ] `02_TOOLS/readme/yt_pipeline.md` — дублирует `pipeline.md`, устарел
- [ ] `00_RAW/Articles/` — пустая папка, скрипт ни разу не запускался

---

## 📦 ПЕРЕЛОЖИТЬ (файлы не там лежат)

- [ ] `02_TOOLS/Booster_Field_Mapping.md` → `04_PROJECTS/AI_Sales_Booster/`
- [ ] `02_TOOLS/Booster_N8N_Schema.md` → `04_PROJECTS/AI_Sales_Booster/`
- [ ] `02_TOOLS/Booster_N8N_Workflow_Blueprint.md` → `04_PROJECTS/AI_Sales_Booster/`
- [ ] `02_TOOLS/Scripts/tg_discovered_sources.md` → `02_TOOLS/`
- [ ] `02_TOOLS/Scripts/tg_discovered_v2.md` → `02_TOOLS/`

---

## ✏️ ОБНОВИТЬ (устарело, но нужно)

- [ ] `02_TOOLS/readme/pipeline.md` — переписать под новый ритм v2.0 (3 потока + 2 авто workflow)
- [ ] `08_IDEAS_LAB/08.1_RAW_IDEAS/08.1.1/` — просмотреть 5 идей, лучшие перевести в `08.2_SELECTED/`, остальные удалить
- [ ] `08_IDEAS_LAB/08.1_RAW_IDEAS/08.1.2/` — то же самое (5 файлов)

---

## ❓ РЕШИТЬ (требует твоего решения, Максим)

- [ ] `TEMPLATES/T_Idea.md`, `T_Project.md`, `T_Recipe.md` — используешь в Obsidian? Если нет — удалить
- [ ] `04_PROJECTS/Content_Marketing_Trofimov/` — только README, папка пустая. Наполнить или удалить?
- [ ] `07_CONSTRUCTION/` — стройпроект (комплекс 20м), не связан с AI Factory. Оставить отдельно или вынести в отдельный репо?

---

## ✅ НЕ ТРОГАТЬ

- Все скрипты в корне: `infra_discovery.py`, `infra_processor.py`, `gold_synthesizer.py`, `processor.py`, `parser_deep.py`, `youtube_parser.py`
- `02_TOOLS/Scripts/` — все рабочие скрипты пайплайна
- `02_TOOLS/crm-ai-product-factory.md`, `crm-ai-ideator.md`
- `02_TOOLS/Content_Factory_Protocol.md`, `Market_Intelligence_Protocol.md`
- `02_TOOLS/claude_gemini_chrome_novpn.md` — полезный рецепт
- `04_PROJECTS/Partner_Marketing/` — активная стратегия
- `04_PROJECTS/AI_Factory_Master_Strategy.md`, `AI_Factory_Setup.md`
- `vern_ideas` — 30 синтезированных продуктов
- `.claude/commands/crm-ai-product-factory.md`
- `.github/workflows/` — все три workflow

---

## 📊 Итог

| Категория | Кол-во |
|---|---|
| Удалить | 8 |
| Переложить | 5 |
| Обновить | 3 |
| Решить | 3 |
| **Итого действий** | **19** |
