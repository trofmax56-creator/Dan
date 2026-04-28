# YouTube Pipeline — Инструкция запуска

## Что делает pipeline

```
GitHub Actions                    Локально (твой ПК)
──────────────────                ──────────────────────────────
yt_discovery.py                   yt_processor_2.py
  └─ ищет видео по запросам         └─ читает 00_RAW/YouTube/
  └─ сохраняет метаданные           └─ скачивает транскрипты
     в 00_RAW/YouTube/              └─ классифицирует GOLD/TRASH
     yt_{id}.md (status: raw)       └─ Claude Haiku извлекает схемы
                                    └─ GOLD → 01_INBOX/Gold/
```

---

## Какие API нужны и где взять

### 1. YOUTUBE_API_KEY
- **Используется:** `yt_discovery.py` (поиск видео через YouTube Data API v3)
- **Где взять:** [console.cloud.google.com](https://console.cloud.google.com)
  1. Создать проект
  2. APIs & Services → Enable APIs → YouTube Data API v3
  3. Credentials → Create API Key
- **Лимит:** 10 000 единиц/день бесплатно (один поиск = 100 единиц = ~100 поисков/день)
- **Где прописать:** GitHub → Settings → Secrets and variables → Actions → New secret → `YOUTUBE_API_KEY`

### 2. ANTHROPIC_API_KEY
- **Используется:** `yt_processor_2.py` (извлечение схем через Claude Haiku)
- **Где взять:** [console.anthropic.com](https://console.anthropic.com) → API Keys
- **Стоимость:** Claude Haiku — примерно $0.001 за одно видео (очень дёшево)
- **Где прописать:** только локально (этот скрипт на GitHub не запускается)

### Примечание: youtube_transcript_api
Библиотека для скачивания субтитров — **ключ не нужен**, работает бесплатно.
Устанавливается один раз: `pip install youtube-transcript-api`

---

## Шаг 1 — Первоначальная настройка (один раз)

```bash
# Установить зависимости
pip install requests youtube-transcript-api anthropic

# Прописать ключи локально (добавить в ~/.bashrc или ~/.zshrc)
export ANTHROPIC_API_KEY="sk-ant-..."
```

В GitHub: Settings → Secrets → Actions → New repository secret
- Name: `YOUTUBE_API_KEY`
- Value: твой ключ из Google Cloud

---

## Шаг 2 — Запуск discovery (GitHub)

1. Открыть репозиторий на GitHub
2. Вкладка **Actions**
3. Слева выбрать **YouTube Discovery**
4. Кнопка **Run workflow** → Run workflow
5. Подождать ~1 минуту
6. После завершения в `00_RAW/YouTube/` появятся новые файлы `yt_{id}.md` со `status: raw`
7. Сделать `git pull` локально чтобы получить новые файлы

---

## Шаг 3 — Запуск processor (локально)

```bash
# Перейти в корень проекта
cd /путь/к/репозиторию

# Запустить обработку
python 02_TOOLS/Scripts/yt_processor_2.py
```

Скрипт выведет примерно:
```
YT Processor запущен (режим: Claude Haiku)
Новых для обработки: 12

  [1/12] Автоматизация Bitrix24 через n8n — кейс...
    GOLD [Claude Haiku]  →  01_INBOX/Gold/yt_abc123.md
  [2/12] Пассивный доход на крипте 2026...
    TRASH
  ...

Готово: GOLD=7 | TRASH=5
```

---

## Что происходит с файлами

### До обработки — `00_RAW/YouTube/yt_{id}.md`
```
status: raw
title, channel, date, url, описание
```

### После обработки — `00_RAW/YouTube/yt_{id}.md`
```
status: gold  (или trash)
+ полный транскрипт видео
```

### Gold-файл — `01_INBOX/Gold/yt_{id}.md`
```
## Суть
## Бизнес-сценарий
## Алгоритм реализации  ← нумерованные шаги с деталями
## Технический стек
## Связки инструментов
## Конфигурация и параметры  ← конкретные значения, эндпоинты
## Ключевые инсайты
## Подводные камни
```

---

## Типичный рабочий ритм

```
Раз в неделю:
1. GitHub Actions → Run workflow  (2 мин)
2. git pull
3. python yt_processor_2.py  (5-15 мин зависит от количества видео)
4. Смотреть новые файлы в 01_INBOX/Gold/
```

---

## Если что-то пошло не так

| Проблема | Причина | Решение |
|---|---|---|
| `Ошибка: задайте YOUTUBE_API_KEY` | Секрет не добавлен в GitHub | Settings → Secrets → YOUTUBE_API_KEY |
| `YouTube блокирует запросы` | Запустил processor на сервере | Запускай только локально |
| `YT Processor (режим: regex)` | Нет ANTHROPIC_API_KEY | `export ANTHROPIC_API_KEY=sk-ant-...` |
| Нет новых файлов после discovery | Все видео уже есть в RAW | Это нормально, дубликаты пропускаются |
