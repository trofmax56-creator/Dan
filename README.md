# 🏭 Dan — Завод ИИ-решений (AI Factory)

> Система автоматического сбора, анализа и упаковки ИИ-решений для бизнеса.
> От парсинга сырых данных до готового продукта и продажи.

**Владелец:** Максим Трофимов | **Студия Трофимов** | Москва

---

## 🗺️ Навигация по репозиторию

### Стартовая точка
| Что хочу сделать | Куда идти |
|---|---|
| Понять всю стратегию целиком | [`04_PROJECTS/AI_Factory_Master_Strategy.md`](04_PROJECTS/AI_Factory_Master_Strategy.md) |
| Запустить сбор новых данных | [`02_TOOLS/readme/pipeline.md`](02_TOOLS/readme/pipeline.md) |
| Выбрать идею для продукта | [`08_IDEAS_LAB/Demand_Matrix.md`](08_IDEAS_LAB/Demand_Matrix.md) |
| Посмотреть готовые рецепты | [`05_BIZ_RECIPES/`](05_BIZ_RECIPES/) |
| Написать пост / контент | [`11_CONTENT FACTORY/11_1_DRAFTS/`](11_CONTENT%20FACTORY/11_1_DRAFTS/) |
| Посмотреть структуру Завода | [`04_PROJECTS/AI_Factory_Setup.md`](04_PROJECTS/AI_Factory_Setup.md) |
| Скоринг Pain+Dev+Profit | [`08_IDEAS_LAB/Demand_Matrix.md`](08_IDEAS_LAB/Demand_Matrix.md) |

---

## 📂 Структура папок

```
Dan/
├── 00_RAW/                    ← Сырые данные (YouTube, Telegram, статьи)
│   ├── YouTube/               ← yt_*.md со status: raw / gold / trash
│   └── Articles/
│
├── 01_INBOX/                  ← Обработанные и отфильтрованные данные
│   ├── Gold/                  ← 407 GOLD-файлов (68 YT + 339 TG)
│   ├── Digest/                ← Аналитические дайджесты
│   └── processed_log.md       ← Лог обработанных ID
│
├── 02_TOOLS/                  ← Скрипты, протоколы, инструменты
│   ├── Scripts/               ← Python-скрипты пайплайна
│   ├── readme/pipeline.md     ← Порядок запуска скриптов
│   ├── crm-ai-ideator.md      ← Скилл генерации идей CRM+AI
│   ├── Content_Factory_Protocol.md  ← Протокол Якорь+Эхо
│   └── Market_Intelligence_Protocol.md ← Критерии отбора источников
│
├── 03_GUIDES/                 ← Техническая документация
│   ├── System_Architecture.md ← Архитектура системы
│   └── clients/               ← Базы знаний по клиентам
│
├── 04_PROJECTS/               ← Активные проекты
│   ├── AI_Factory_Master_Strategy.md ← ⭐ ГЛАВНЫЙ РЕФЕРЕНС
│   └── AI_Factory_Setup.md    ← Структура 4 цехов Завода
│
├── 05_BIZ_RECIPES/            ← Библиотека готовых решений (15 рецептов)
│   └── 0XX_название.md        ← Каждый рецепт = ТЗ + КП + скрипт продаж
│
├── 08_IDEAS_LAB/              ← Лаборатория идей
│   ├── Demand_Matrix.md       ← Скоринг Pain+Dev+Profit
│   ├── 08.1_RAW_IDEAS/        ← Сырые идеи из GOLD
│   ├── 08.2_SELECTED/         ← Отобранные для реализации
│   └── 08.3_IMPLEMENTATION_PLANS/ ← Планы реализации
│
├── 11_CONTENT FACTORY/        ← Контент-фабрика
│   ├── 11_1_DRAFTS/           ← Черновики постов и статей
│   └── 11_2_n8n_Content/      ← n8n-контент
│
├── .github/workflows/
│   └── yt_discovery.yml       ← CI/CD: сбор + обработка YouTube
│
├── CLAUDE.md                  ← Инструкции для AI-агента
├── Dan_Manual.md              ← Правила работы системы
└── README.md                  ← Этот файл
```

---

## ⚙️ Скрипты пайплайна

| Скрипт | Назначение | Запуск | Ключи |
|---|---|---|---|
| `yt_discovery.py` | Сбор YouTube видео | GitHub Actions | `YOUTUBE_API_KEY` |
| `yt_processor_2.py` | Классификация + Claude Haiku | GitHub Actions | `ANTHROPIC_API_KEY` |
| `tg_discovery.py` | Сбор постов Telegram | Локально | Telegram сессия |
| `tg_discovery_v2.py` | Новые TG-каналы | Локально | Telegram сессия |
| `article_discovery.py` | Статьи Habr/VC.ru | Локально | `FIRECRAWL_API_KEY` |

### Быстрый запуск YouTube-пайплайна
```
GitHub → Actions → YouTube Discovery → Run workflow
```
После завершения:
```bash
git pull
```

---

## 🔄 Конвейер (полная схема)

```
СБОР                  ОБРАБОТКА             ОТБОР
────────────          ────────────          ────────────
yt_discovery    →     yt_processor_2  →     Demand Matrix
tg_discovery    →     (в разработке)  →     Pain+Dev+Profit
article_disc.   →     (в разработке)  →     Роутинг по цехам
      ↓                     ↓                     ↓
00_RAW/             01_INBOX/Gold/          04_PROJECTS/
                                            05_BIZ_RECIPES/
                                            08_IDEAS_LAB/
                                            11_1_DRAFTS/

УПАКОВКА              РАЗРАБОТКА            МАРКЕТИНГ → ПРОДАЖА
────────────          ────────────          ────────────────────
BIZ_RECIPE      →     n8n workflow    →     Habr/VC.ru (Якорь)
crm-ai-ideator        self-hosted n8n       TG/TenChat/ВК (Эхо)
Шаблон ТЗ+КП          Docker/VPS            → Лид → Демо → Договор
```

---

## 🔑 API-ключи

| Ключ | Где хранится | Для чего |
|---|---|---|
| `YOUTUBE_API_KEY` | GitHub Secrets | yt_discovery.py |
| `ANTHROPIC_API_KEY` | GitHub Secrets | yt_processor_2.py + Claude API |
| `FIRECRAWL_API_KEY` | Локально (.env) | article_discovery.py |
| Telegram сессия | `dan_session` в корне | tg_discovery*.py |

---

## 📊 Текущее состояние

| Метрика | Значение |
|---|---|
| GOLD-файлов в 01_INBOX | **407** (68 YT + 339 TG) |
| BIZ_RECIPES готовых | **15** (051–065) |
| Цель по рецептам | **30+** |
| Продуктов в работе | в процессе скоринга |

---

## 📅 Недельный ритм

| День | Действие | Время |
|---|---|---|
| Понедельник | Run workflow → git pull | 15 мин |
| Вторник | Скоринг новых GOLD по Demand Matrix | 1–2 ч |
| Среда | Упаковка 1–2 BIZ_RECIPE + черновик поста | 2–3 ч |
| Четверг | Сборка n8n workflow по рецепту | весь день |
| Пятница | Публикация якоря (Habr/VC.ru) + эхо | 1 ч |
| Раз в 2 нед. | tg_discovery + article_discovery | 30 мин |

---

*Главный документ проекта: [`04_PROJECTS/AI_Factory_Master_Strategy.md`](04_PROJECTS/AI_Factory_Master_Strategy.md)*
