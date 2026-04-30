# 🏭 Dan — Завод ИИ-решений (AI Factory)

> Система автоматического сбора, анализа и упаковки ИИ-решений для бизнеса.
> От парсинга сырых данных до готового продукта и продажи.

**Владелец:** Максим Трофимов | **Студия Трофимов** | Москва
**Версия:** 2.0 | **Обновлено:** 2026-04-30

---

## 🗺️ Навигация

| Что хочу сделать | Куда идти |
|---|---|
| Понять всю стратегию целиком | [`04_PROJECTS/AI_Factory_Master_Strategy.md`](04_PROJECTS/AI_Factory_Master_Strategy.md) |
| Посмотреть готовые продукты | [`05_BIZ_RECIPES/`](05_BIZ_RECIPES/) |
| Отобрать идею для следующего спринта | [`08_IDEAS_LAB/08.2_SELECTED/`](08_IDEAS_LAB/08.2_SELECTED/) |
| Написать пост / контент | [`11_CONTENT FACTORY/11_1_DRAFTS/`](11_CONTENT%20FACTORY/11_1_DRAFTS/) |
| Структура 5 цехов Завода | [`04_PROJECTS/AI_Factory_Setup.md`](04_PROJECTS/AI_Factory_Setup.md) |
| Дайджест идей этой недели | [`01_INBOX/Gold/infra_digest_*.md`](01_INBOX/Gold/) |
| Дайджест продуктов из Gold | [`08_IDEAS_LAB/08.2_SELECTED/products_digest_*.md`](08_IDEAS_LAB/08.2_SELECTED/) |

---

## 📂 Структура папок

```
Dan/
├── 00_RAW/                    ← Сырые данные
│   ├── Telegram/              ← посты из TG-каналов
│   ├── YouTube/               ← видео из YT-каналов
│   ├── Infra/                 ← infra_discovery JSON + MD дайджесты
│   └── Articles/              ← статьи Habr/VC.ru
│
├── 01_INBOX/                  ← Обработанные данные
│   ├── Gold/                  ← 600+ GOLD-файлов (TG + YT + Infra дайджесты)
│   └── processed_log.md       ← Лог обработанных ID
│
├── 02_TOOLS/                  ← Инструменты и протоколы
│   ├── Scripts/               ← Python-скрипты пайплайна
│   ├── crm-ai-product-factory.md  ← Стандарт продукта (9 пунктов)
│   ├── crm-ai-ideator.md      ← Векторы генерации идей
│   ├── Content_Factory_Protocol.md
│   └── Market_Intelligence_Protocol.md
│
├── 04_PROJECTS/               ← Активные проекты и стратегия
│   ├── AI_Factory_Master_Strategy.md  ← ⭐ ГЛАВНЫЙ РЕФЕРЕНС
│   └── AI_Factory_Setup.md    ← Структура 5 цехов
│
├── 05_BIZ_RECIPES/            ← 108+ готовых продуктов
│   ├── 051–082_*.md           ← Ручные рецепты (YT-каналы)
│   ├── 083–108_infra_*.md     ← Из infra_processor (YouTube поиск)
│   └── 1XX_gold_*.md          ← Из gold_synthesizer (синтез Gold)
│
├── 08_IDEAS_LAB/              ← Лаборатория идей
│   ├── Demand_Matrix.md
│   ├── 08.1_RAW_IDEAS/        ← score < 20
│   ├── 08.2_SELECTED/         ← score 20–24, products_digest_*.md
│   └── 08.3_IMPLEMENTATION_PLANS/
│
├── 11_CONTENT FACTORY/
│   ├── 11_1_DRAFTS/           ← Черновики постов
│   └── 11_2_n8n_Content/
│
├── .claude/commands/
│   └── crm-ai-product-factory.md  ← /crm-ai-product-factory slash-команда
│
├── .github/workflows/
│   ├── yt_discovery.yml       ← YouTube-каналы (вручную)
│   ├── infra_discovery.yml    ← Поиск по 60 запросам (пн 09:00 МСК)
│   └── gold_synthesizer.yml   ← Синтез Gold → продукты (вс 08:00 МСК)
│
├── infra_discovery.py         ← YouTube API, 60 запросов, → 00_RAW/Infra/
├── infra_processor.py         ← Claude → паспорта идей из Infra
├── gold_synthesizer.py        ← Claude → продукты из Gold (формат vern_ideas)
├── processor.py               ← Классификация TG → Gold
├── parser_deep.py             ← Telegram парсер (локально)
├── youtube_parser.py          ← YouTube RSS (каналы)
├── vern_ideas                 ← 30 продуктов, синтезированных агентом
└── CLAUDE.md                  ← Инструкции для AI-агента
```

---

## ⚙️ Скрипты и потоки

### Поток 1 — Telegram (вручную, раз в 2 недели)
```
parser_deep.py → 00_RAW/Telegram/ → processor.py → 01_INBOX/Gold/
```

### Поток 2 — YouTube-каналы (вручную через GitHub Actions)
```
youtube_parser.py → 00_RAW/YouTube/ → yt_processor_2.py → 01_INBOX/Gold/
```

### Поток 3 — Infra Discovery (авто, каждый понедельник)
```
infra_discovery.py → 00_RAW/Infra/ → infra_processor.py
  → 05_BIZ_RECIPES/ (score ≥22)
  → 08_IDEAS_LAB/08.2_SELECTED/ (score 18–21)
  → 01_INBOX/Gold/infra_digest_*.md
```

### Поток 4 — Gold Synthesizer (авто, каждое воскресенье)
```
01_INBOX/Gold/ (последние 40 файлов) → gold_synthesizer.py → Claude
  → 05_BIZ_RECIPES/ (score >24)
  → 08_IDEAS_LAB/08.2_SELECTED/ (score 20–24)
  → 08_IDEAS_LAB/08.2_SELECTED/products_digest_*.md
```

---

## 🤖 GitHub Actions

| Workflow | Триггер | Что делает |
|---|---|---|
| `yt_discovery.yml` | Вручную | YouTube-каналы → Gold |
| `infra_discovery.yml` | **Авто пн 09:00 МСК** + вручную | 60 запросов → паспорта идей |
| `gold_synthesizer.yml` | **Авто вс 08:00 МСК** + вручную | Gold → синтез продуктов |

### Ручной запуск
```
GitHub → Actions → [название workflow] → Run workflow
```

---

## 🔑 API-ключи

| Ключ | Где хранится | Используется в |
|---|---|---|
| `ANTHROPIC_API_KEY` | GitHub Secrets | infra_processor, gold_synthesizer, yt_processor |
| `YOUTUBE_API_KEY` | GitHub Secrets | infra_discovery, yt_discovery |
| Telegram сессия | `dan_session` в корне | parser_deep.py (только локально) |

---

## 📊 Текущее состояние

| Метрика | Значение |
|---|---|
| GOLD-файлов в 01_INBOX | **600+** |
| BIZ_RECIPES готовых | **108+** (051–108) |
| SELECTED в Ideas Lab | **130+** |
| Продуктов-идей (vern_ideas) | **30** |
| Автоматических потоков | **2** (infra + gold, еженедельно) |

---

## 📅 Недельный ритм

| День | Действие | Участие Максима |
|---|---|---|
| Воскресенье | Gold Synthesizer — авто | — |
| Понедельник | Infra Discovery — авто | `git pull` — 5 мин |
| Вторник | Разбор дайджестов, выбор продукта в работу | 30–60 мин |
| Среда–Четверг | Сборка n8n workflow по BIZ_RECIPE | Разработка |
| Пятница | Публикация контента (якорь + эхо) | 1 час |
| Раз в 2 нед. | `parser_deep.py` + `youtube_parser.py` (локально) | 15 мин |

---

*Главный документ: [`04_PROJECTS/AI_Factory_Master_Strategy.md`](04_PROJECTS/AI_Factory_Master_Strategy.md)*
