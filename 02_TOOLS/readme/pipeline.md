# Pipeline парсинга — все скрипты по порядку

## Схема работы

```
ПОИСК КОНТЕНТА                    ОБРАБОТКА / ФИЛЬТРАЦИЯ
──────────────────────────        ──────────────────────────────────
1. yt_discovery.py                4. yt_processor_2.py
   GitHub Actions → вручную          Локально → вручную
   00_RAW/YouTube/                    00_RAW/YouTube/ → 01_INBOX/Gold/

2. tg_discovery.py                (Telegram обработка — в разработке)
   Локально → вручную
   → tg_discovered_sources.md

3. tg_discovery_v2.py             (Статьи обработка — в разработке)
   Локально → вручную
   → tg_discovered_v2.md

   article_discovery.py
   Локально → вручную
   00_RAW/Articles/
```

---

## Шаг 1 — yt_discovery.py
**Что делает:** Ищет видео на YouTube по запросам, сохраняет метаданные в `00_RAW/YouTube/`

**Где запускать:** GitHub Actions (вручную)

**Нужные ключи:**
- `YOUTUBE_API_KEY` → GitHub Secrets

**Запуск:**
1. GitHub → Actions → YouTube Discovery → Run workflow
2. После завершения — `git pull` локально

**Результат:** Новые файлы `yt_{id}.md` со `status: raw` в `00_RAW/YouTube/`

---

## Шаг 2 — yt_processor_2.py
**Что делает:**
- Читает файлы `yt_*.md` со `status: raw` из `00_RAW/YouTube/`
- Скачивает транскрипт видео
- Классифицирует GOLD / TRASH по ключевым словам
- GOLD → извлекает алгоритм, стек, конфиг через Claude Haiku
- Сохраняет в `01_INBOX/Gold/yt_{id}.md`
- Обновляет статус в raw-файле на `gold` или `trash`

**Где запускать:** Локально (YouTube блокирует транскрипты на серверах)

**Нужные ключи:**
- `ANTHROPIC_API_KEY` (Claude Haiku — ~$0.001 за видео)

**Запуск (Windows cmd):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
python 02_TOOLS/Scripts/yt_processor_2.py
```

**Запуск (Mac/Linux):**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
python 02_TOOLS/Scripts/yt_processor_2.py
```

**Результат:** Gold-файлы с полным алгоритмом реализации в `01_INBOX/Gold/`

---

## Шаг 3 — tg_discovery.py
**Что делает:** Ищет посты в Telegram по ключевым словам об автоматизации/CRM/AI. Фильтрует спам по чёрному/белому спискам.

**Где запускать:** Локально (нужна активная Telegram-сессия)

**Нужные ключи:**
- Telegram API_ID и API_HASH (уже прописаны в скрипте)
- Активная сессия `dan_session` в корне проекта

**Запуск:**
```bash
python 02_TOOLS/Scripts/tg_discovery.py
```

**Результат:** `02_TOOLS/Scripts/tg_discovered_sources.md` — список каналов с Gold-постами

---

## Шаг 4 — tg_discovery_v2.py
**Что делает:** Находит новые Telegram-каналы через граф упоминаний от уже известных каналов. Исключает уже известные источники.

**Где запускать:** Локально

**Нужные ключи:**
- Та же Telegram-сессия

**Запуск:**
```bash
python 02_TOOLS/Scripts/tg_discovery_v2.py
```

**Результат:** `02_TOOLS/Scripts/tg_discovered_v2.md` — новые каналы для мониторинга

---

## Шаг 5 — article_discovery.py
**Что делает:** Скрапит статьи с habr.com и vc.ru по тегам (n8n, CRM, API, Bitrix24 и др.). Сохраняет сырые статьи.

**Где запускать:** Локально

**Нужные ключи:**
- `FIRECRAWL_API_KEY` → console.firecrawl.dev

**Запуск:**
```bash
export FIRECRAWL_API_KEY=fc-...
python 02_TOOLS/Scripts/article_discovery.py
```

**Результат:** Статьи в `00_RAW/Articles/`

---

## Типичный недельный ритм

```
ПОНЕДЕЛЬНИК (5 мин — GitHub)
  → yt_discovery.py  [Run workflow]
  → git pull

ВТОРНИК-СРЕДА (15-20 мин — локально)
  → yt_processor_2.py  [обработка новых видео → Gold]

РАЗ В 2 НЕДЕЛИ (локально)
  → tg_discovery.py   [новые посты Telegram]
  → tg_discovery_v2.py  [новые каналы]
  → article_discovery.py  [статьи habr/vc.ru]
```

---

## Нужные API ключи — итого

| Ключ | Для чего | Где взять | Платно? |
|---|---|---|---|
| `YOUTUBE_API_KEY` | yt_discovery.py | console.cloud.google.com | Бесплатно (лимит 10k/день) |
| `ANTHROPIC_API_KEY` | yt_processor_2.py | console.anthropic.com | ~$0.001/видео |
| `FIRECRAWL_API_KEY` | article_discovery.py | firecrawl.dev | Есть бесплатный план |
| Telegram сессия | tg_discovery*.py | Уже есть в проекте | Бесплатно |
