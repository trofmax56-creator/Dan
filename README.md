# 🏭 Dan — Завод ИИ-решений (AI Factory)

> Система автоматического сбора, анализа и упаковки ИИ-решений для бизнеса.
> От парсинга сырых данных до готового продукта и продажи.

**Владелец:** Максим Трофимов | **Студия Трофимов** | Москва
**Версия:** 3.1 | **Обновлено:** 2026-05-02

---

## 🗺️ Навигация

| Что хочу сделать | Куда идти |
|---|---|
| Понять всю стратегию целиком | [`04_PROJECTS/AI_Factory_Master_Strategy.md`](04_PROJECTS/AI_Factory_Master_Strategy.md) |
| Посмотреть готовые продукты | [`05_BIZ_RECIPES/`](05_BIZ_RECIPES/) |
| Отобрать идею для следующего спринта | [`08_IDEAS_LAB/08.2_SELECTED/`](08_IDEAS_LAB/08.2_SELECTED/) |
| Написать пост / контент | [`11_CONTENT FACTORY/11_1_DRAFTS/`](11_CONTENT%20FACTORY/11_1_DRAFTS/) |
| Структура 5 цехов Завода | [`04_PROJECTS/AI_Factory_Setup.md`](04_PROJECTS/AI_Factory_Setup.md) |
| Свежий GOLD CRM этой недели | [`01_INBOX/Gold/`](01_INBOX/Gold/) |
| Инструменты, платформы, vibe coding | [`01_INBOX/Gold_Tools/`](01_INBOX/Gold_Tools/) |
| 30 синтезированных продуктов | [`04_PROJECTS/vern_ideas.md`](04_PROJECTS/vern_ideas.md) |

---

## 📂 Структура папок

```
Dan/
├── 00_RAW/                    ← Сырые данные
│   ├── Telegram/              ← посты из TG-каналов (27 каналов)
│   ├── YouTube/               ← видео из YT-каналов (RSS + API)
│   └── Articles/              ← будущий поток (Habr/VC.ru)
│
├── 01_INBOX/                  ← Обработанные данные
│   ├── Gold/                  ← 336 CRM-файлов → gold_synthesizer
│   ├── Gold_Tools/            ← 58 файлов (vibe coding, платформы, гайды) — не в synthesizer
│   └── processed_log.md       ← Лог обработанных ID
│
├── 02_TOOLS/                  ← Инструменты и протоколы
│   ├── Scripts/               ← Python-скрипты пайплайна
│   │   ├── tg_discovery_v2.py ← Поиск новых TG-каналов (граф-обход)
│   │   ├── yt_discovery.py    ← YouTube API поиск (GitHub Actions)
│   │   └── yt_processor_2.py  ← Claude Haiku → Gold из YT
│   ├── crm-ai-product-factory.md  ← Стандарт продукта v3.0 (9 пунктов)
│   ├── crm-ai-ideator.md      ← Векторы генерации идей
│   ├── Content_Factory_Protocol.md
│   └── Market_Intelligence_Protocol.md
│
├── 04_PROJECTS/               ← Активные проекты и стратегия
│   ├── AI_Factory_Master_Strategy.md  ← ⭐ ГЛАВНЫЙ РЕФЕРЕНС
│   ├── AI_Factory_Setup.md    ← Структура 5 цехов
│   └── vern_ideas.md          ← 30 синтезированных AI-продуктов (референс)
│
├── 05_BIZ_RECIPES/            ← Готовые продукты (score > 24, v3.0)
│
├── 08_IDEAS_LAB/              ← Лаборатория идей
│   ├── 08.1_RAW_IDEAS/        ← score 18–19
│   ├── 08.2_SELECTED/         ← score 20–24
│   └── 08.3_IMPLEMENTATION_PLANS/
│
├── 11_CONTENT FACTORY/
│   ├── 11_1_DRAFTS/           ← Черновики постов
│   └── 11_2_n8n_Content/
│
├── _ARCHIVE/                  ← Архив (не используется)
│   ├── infra/                 ← Старый infra-пайплайн
│   ├── old_biz_recipes/       ← BIZ_RECIPES до v3.0
│   ├── old_ideas_lab/         ← Ideas Lab до v3.0
│   └── old_scripts/           ← parser_deep.py, tg_discovery_v1.py и др.
│
├── .claude/commands/
│   └── crm-ai-product-factory.md  ← /crm-ai-product-factory slash-команда
│
├── .github/workflows/
│   ├── yt_discovery.yml       ← YouTube-каналы (вручную)
│   └── gold_synthesizer.yml   ← Синтез Gold → продукты (вс 08:00 МСК)
│
├── parser.py                  ← Telegram парсер (27 каналов, локально)
├── processor.py               ← Классификация TG → Gold_CRM / Gold_Tools (без API)
├── youtube_parser.py          ← YouTube RSS (10 каналов, локально)
├── gold_synthesizer.py        ← Claude → продукты из Gold_CRM (GitHub Actions, v2.0)
└── CLAUDE.md                  ← Инструкции для AI-агента
```

---

## ⚙️ Скрипты и потоки

### Поток 1 — Telegram (вручную, раз в 2 недели)
```
parser.py → 00_RAW/Telegram/
  → processor.py (разветвление по ключевым словам)
      ├── GOLD_CRM  → 01_INBOX/Gold/       ← идёт в gold_synthesizer
      └── GOLD_TOOLS → 01_INBOX/Gold_Tools/ ← инструменты/платформы, не в synthesizer
```
Без API-расходов. Локально.

**Логика разветвления processor.py:**
- Есть CRM-якорь (`bitrix`, `n8n`, `crm`, `webhook`) → `Gold/`
- Только инструментальные слова (`cursor`, `langgraph`, `emergent`, `dify`, `vibe coding`) → `Gold_Tools/`
- Ничего не совпало → TRASH

### Поток 2 — YouTube RSS (вручную, раз в 2 недели)
```
youtube_parser.py → 00_RAW/YouTube/
```
Без API-расходов. Локально.

### Поток 3 — YouTube API (вручную через GitHub Actions)
```
yt_discovery.py → 00_RAW/YouTube/ → yt_processor_2.py → 01_INBOX/Gold/
```
Использует Claude Haiku + YouTube Data API.

### Поток 4 — Gold Synthesizer (авто, каждое воскресенье)
```
01_INBOX/Gold/ (последние 40 файлов) → gold_synthesizer.py → Claude Sonnet
  → 05_BIZ_RECIPES/        (score > 24)
  → 08_IDEAS_LAB/08.2_SELECTED/ (score 20–24)
  → 08_IDEAS_LAB/08.1_RAW_IDEAS/ (score 18–19)
```
Стоимость: ~$0.15–0.35 за запуск. `Gold_Tools/` synthesizer не читает.

---

## 🔍 Поиск новых TG-каналов

```
python 02_TOOLS/Scripts/tg_discovery_v2.py
```
Читает упоминания t.me/ в `00_RAW/Telegram/`, проверяет каналы через Telethon,
фильтрует по BLACKLIST. Результат → `tg_discovered_v2.md`. Новые каналы добавляются
вручную в `parser.py`.

---

## 🤖 GitHub Actions

| Workflow | Триггер | Что делает |
|---|---|---|
| `yt_discovery.yml` | Вручную | YouTube-каналы → Gold |
| `gold_synthesizer.yml` | **Авто вс 08:00 МСК** + вручную | Gold_CRM → синтез продуктов |

### Ручной запуск
```
GitHub → Actions → [название workflow] → Run workflow
```

---

## 🔑 API-ключи

| Ключ | Где хранится | Используется в |
|---|---|---|
| `ANTHROPIC_API_KEY` | GitHub Secrets | gold_synthesizer, yt_processor_2 |
| `YOUTUBE_API_KEY` | GitHub Secrets | yt_discovery |
| Telegram сессия | `dan_session` в корне | parser.py (только локально) |

---

## 📊 Текущее состояние

| Метрика | Значение |
|---|---|
| Gold CRM (→ synthesizer) | **336** файлов |
| Gold Tools (инструменты) | **58** файлов |
| BIZ_RECIPES готовых | **0** (v3.0, пустые — ждут воскресенья) |
| Telegram-каналов | **27** |
| YouTube RSS-каналов | **10** |
| Автоматических потоков | **1** (gold_synthesizer, еженедельно) |

---

## 📅 Недельный ритм

| Когда | Действие | Участие Максима |
|---|---|---|
| Воскресенье (авто) | Gold Synthesizer → новые BIZ_RECIPES | — |
| Понедельник | `git pull` → разобрать новые BIZ_RECIPES | 30 мин |
| Среда–Четверг | Сборка n8n workflow по BIZ_RECIPE | Разработка |
| Пятница | Публикация контента (якорь + эхо) | 1 час |
| Раз в 2 нед. | `parser.py` + `processor.py` + `youtube_parser.py` (локально) | 15 мин |

---

*Главный документ: [`04_PROJECTS/AI_Factory_Master_Strategy.md`](04_PROJECTS/AI_Factory_Master_Strategy.md)*
