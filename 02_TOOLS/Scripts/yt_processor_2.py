import re
import os
import json
import time
from pathlib import Path
from datetime import date

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled, RequestBlocked
except ImportError:
    print("Установи библиотеку: pip install youtube-transcript-api")
    exit(1)

try:
    import anthropic as anthropic_lib
    _claude = anthropic_lib.Anthropic() if os.environ.get("ANTHROPIC_API_KEY") else None
except ImportError:
    _claude = None

_yt_api = YouTubeTranscriptApi()

BASE_DIR = Path(__file__).parent.parent.parent
RAW_YT_DIR = BASE_DIR / "00_RAW" / "YouTube"
GOLD_CRM_DIR = BASE_DIR / "01_INBOX" / "Gold"        # → gold_synthesizer (продукты CRM)
GOLD_TOOLS_DIR = BASE_DIR / "01_INBOX" / "Gold_Tools"  # → справочник инструментов
PROCESSED_LOG = BASE_DIR / "01_INBOX" / "processed_log.md"

GOLD_CRM_DIR.mkdir(parents=True, exist_ok=True)
GOLD_TOOLS_DIR.mkdir(parents=True, exist_ok=True)

# ── GOLD_CRM — бизнес-автоматизация, CRM-интеграции (→ gold_synthesizer) ──────
GOLD_CRM_KEYWORDS = [
    "n8n", "make.com", "zapier", "workflow", "автоматизация", "автоматизировать",
    "bitrix", "amocrm", "retailcrm", "1с", "crm", "интеграция", "интегратор",
    "api", "webhook",
    "агент", "agent", "prompt", "промпт",
    "claude", "chatgpt", "gpt-", "openai", "anthropic", "gemini", "llm",
    "нейросет", "нейронн", "модель", "релиз",
    "python", "langchain", "rag", "vector", "embeddings",
    "кейс", "схема", "гайд", "инструкция", "пошагово", "туториал",
    "obsidian", "notion", "второй мозг",
    "аналитик", "дашборд", "визуализаци", "метрик",
]

# ── GOLD_TOOLS — инструменты, платформы, вайбкодинг (→ Gold_Tools) ────────────
GOLD_TOOLS_KEYWORDS = [
    # Мультиагентные системы
    "мультиагент", "multiagent", "multi-agent", "агентная архитектур",
    "langgraph", "crewai", "autogen", "оркестратор",
    # Vibe coding и AI-IDE
    "вайбкодинг", "vibecoding", "vibe coding", "vibe-coding",
    "cursor", "windsurf", "bolt", "lovable", "replit", "claude code", "copilot",
    # Новые AI-платформы
    "emergent", "same.dev", "v0.dev", "vercel ai", "atoms",
    "dify", "flowise", "langflow",
    # Установка и деплой
    "деплой", "deploy", "self-hosted", "установка", "настройк", "docker compose",
    # Модели нового поколения
    "deepseek", "mistral", "qwen", "llama", "ollama", "sonnet", "opus", "gpt-5",
    # Контент и публикации
    "контент", "публикаци", "постинг",
]

# ── CRM-якоря: если есть — всегда GOLD_CRM ────────────────────────────────────
CRM_ANCHORS = ["bitrix", "amocrm", "retailcrm", "crm", "n8n", "make.com", "webhook", "интеграц"]

TRASH_KEYWORDS = [
    "крипт", "биткоин", "токен", "nft", "майнинг", "трейдинг",
    "заработок", "заработай", "пассивный доход", "доход от",
    "похудей", "похудение", "диет", "астролог", "гадани",
    "ретрит", "медитаци", "эзотерик", "нейрографик",
    "подработка", "казино", "ставки", "форекс",
    "скидка", "акция", "промокод", "реклама",
]

TOOLS = [
    "n8n", "make.com", "zapier", "telegram", "whatsapp", "notion", "obsidian",
    "claude", "chatgpt", "gpt", "gemini", "openai", "anthropic",
    "bitrix24", "amocrm", "retailcrm", "1с", "python", "langchain",
    "api", "webhook", "http", "rest", "graphql",
    "google sheets", "airtable", "postgresql", "mysql", "redis",
    "docker", "vps", "server", "github",
]

CLAUDE_SYSTEM = """Ты — технический эксперт по автоматизации бизнеса.
Твоя задача — извлечь из транскрипта YouTube-видео максимально полную техническую документацию.
Пользователь будет читать твой анализ и по нему с нуля воспроизводить автоматизацию.
Поэтому извлекай ВСЕ технические детали: конкретные шаги с подробностями, названия нод и полей,
значения параметров, эндпоинты API, логику условий, типичные ошибки.
Если автор что-то настраивает на экране — опиши что именно и какие значения выставляет.
Отвечай строго на русском языке."""

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "main_idea": {
            "type": "string",
            "description": "Что конкретно автоматизируется, зачем и какой бизнес-результат даёт — 2-3 предложения",
        },
        "use_case": {
            "type": "string",
            "description": "Бизнес-сценарий: кто использует, какую задачу решает, какие данные обрабатывает",
        },
        "workflow": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Детальный пошаговый алгоритм реализации. Каждый элемент — один шаг с конкретными действиями и настройками. Минимум 5 шагов.",
        },
        "tech_stack": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Полный список инструментов, сервисов, API, библиотек — всё что используется в связке",
        },
        "tech_links": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Технические связки с направлением данных. Пример: 'Webhook → n8n → Claude API → Bitrix24'",
        },
        "config_details": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Конкретные настройки: названия нод, параметры, значения полей, эндпоинты, токены, форматы данных упомянутые в видео",
        },
        "key_insights": {
            "type": "array",
            "items": {"type": "string"},
            "description": "6-10 практических выводов: конкретные факты, цифры, хаки, неочевидные приёмы",
        },
        "gotchas": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Подводные камни, типичные ошибки, ограничения о которых предупреждает автор",
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Теги: n8n, make.com, zapier, Claude, ChatGPT, Gemini, LangChain, RAG, AI-агент, автоматизация, Bitrix24, amoCRM, Python, API, workflow",
        },
    },
    "required": ["main_idea", "use_case", "workflow", "tech_stack", "tech_links", "config_details", "key_insights", "gotchas", "tags"],
    "additionalProperties": False,
}


# --- Парсинг raw-файлов ---

def parse_frontmatter(content: str) -> dict:
    fm = {}
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return fm
    for line in m.group(1).split("\n"):
        kv = re.match(r"^(\w+):\s*(.+)$", line)
        if kv:
            fm[kv.group(1).strip()] = kv.group(2).strip()
    return fm


def parse_raw_dir() -> list[dict]:
    videos = []
    for filepath in sorted(RAW_YT_DIR.glob("yt_*.md")):
        content = filepath.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        if fm.get("status") != "raw":
            continue
        video_id = fm.get("video_id", "")
        if not video_id:
            continue
        desc_match = re.search(r"## Описание\n(.+?)(?:\n##|$)", content, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else ""
        videos.append({
            "video_id": video_id,
            "title": fm.get("title", ""),
            "channel": fm.get("channel", ""),
            "date": fm.get("date", ""),
            "url": fm.get("url", ""),
            "description": description,
            "filepath": filepath,
            "content": content,
        })
    return videos


def update_raw_file(filepath: Path, content: str, status: str, transcript: str):
    updated = content.replace("\nstatus: raw\n", f"\nstatus: {status.lower()}\n", 1)
    snippet = transcript[:8000] if len(transcript) > 8000 else transcript
    updated += f"\n## Транскрипт\n{snippet}\n"
    filepath.write_text(updated, encoding="utf-8")


def update_processed_log(new_ids: list):
    today = date.today().strftime("%Y-%m-%d")
    entry = f"\n### YouTube ({len(new_ids)} видео) — {today}\n"
    entry += ", ".join(new_ids) + "\n"
    with open(PROCESSED_LOG, "a", encoding="utf-8") as f:
        f.write(entry)


# --- Транскрипт ---

_yt_blocked = False  # показываем предупреждение только один раз

def fetch_transcript(video_id: str) -> str:
    global _yt_blocked
    try:
        transcript = _yt_api.fetch(video_id, languages=["ru", "en"])
        return " ".join(entry.text for entry in transcript)
    except RequestBlocked:
        if not _yt_blocked:
            print("  ⚠️  YouTube блокирует транскрипты — классификация по заголовку и описанию.")
            _yt_blocked = True
        return ""
    except (NoTranscriptFound, TranscriptsDisabled):
        return ""
    except Exception as e:
        print(f"  Ошибка транскрипта {video_id}: {e}")
        return ""


# --- Классификация ---

def classify(text: str) -> str:
    """Возвращает: GOLD_CRM | GOLD_TOOLS | TRASH"""
    text_lower = text.lower()
    trash_score = sum(1 for kw in TRASH_KEYWORDS if kw in text_lower)
    if trash_score >= 2:
        return "TRASH"

    crm_score = sum(1 for kw in GOLD_CRM_KEYWORDS if kw in text_lower)
    tools_score = sum(1 for kw in GOLD_TOOLS_KEYWORDS if kw in text_lower)
    has_crm_anchor = any(a in text_lower for a in CRM_ANCHORS)

    if has_crm_anchor and crm_score >= 1:
        return "GOLD_CRM"
    if crm_score >= 2:
        return "GOLD_CRM"
    if tools_score >= 2:
        return "GOLD_TOOLS"
    if tools_score == 1 and trash_score == 0:
        return "GOLD_TOOLS"
    if crm_score == 1 and trash_score == 0:
        return "GOLD_CRM"
    return "TRASH"


# --- Извлечение через Claude Haiku ---

def extract_with_claude(text: str, title: str) -> dict | None:
    if not _claude:
        return None
    content = text[:20000] if len(text) > 20000 else text
    user_prompt = f"Заголовок видео: {title}\n\nТранскрипт:\n{content}"
    try:
        response = _claude.messages.create(
            model="claude-haiku-4-5",
            max_tokens=2048,
            system=[{
                "type": "text",
                "text": CLAUDE_SYSTEM,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_prompt}],
            tools=[{
                "name": "extract_video_info",
                "description": "Извлечь структурированную информацию из транскрипта YouTube-видео",
                "input_schema": EXTRACTION_SCHEMA,
            }],
            tool_choice={"type": "tool", "name": "extract_video_info"},
        )
        result = next((b.input for b in response.content if b.type == "tool_use"), None)
        if not result:
            return None
        usage = response.usage
        cached = getattr(usage, "cache_read_input_tokens", 0)
        if cached:
            print(f"    💾 Кэш: {cached} токенов сэкономлено")
        return result
    except Exception as e:
        print(f"    ⚠️  Claude API ошибка: {e}")
        return None


# --- Regex fallback ---

def _regex_main_idea(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    return sentences[0] if sentences else text[:200]


def _regex_schema(text: str) -> str:
    lines = text.split("\n")
    schema_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(m in line for m in ["→", "->", "➡", "⟶", "▶"]):
            schema_lines.append(line)
        elif re.match(r"^\d+[\.\)]\s", line):
            schema_lines.append(line)
        elif any(w in line.lower() for w in ["шаг", "сначала", "затем", "потом", "далее"]):
            schema_lines.append(line)
    return "\n".join(schema_lines[:8]) if schema_lines else "_Не описана_"


def _regex_tech_links(text: str) -> list:
    text_lower = text.lower()
    found = [t for t in TOOLS if t in text_lower]
    if len(found) < 2:
        return found
    links = []
    for sentence in re.split(r"[.!?\n]", text_lower):
        tools_in = [t for t in found if t in sentence]
        if len(tools_in) >= 2:
            link = " → ".join(tools_in[:3])
            if link not in links:
                links.append(link)
    return links[:5] if links else found[:4]


def _regex_meat(text: str) -> list:
    lines = text.split("\n")
    result = []
    for line in lines:
        line = line.strip()
        if len(line) < 20:
            continue
        has_numbers = bool(re.search(r"\d+[%\+\-×xX]|\d{4,}|\d+\s*(руб|тыс|млн|мин|час|сек)", line))
        has_tech = any(kw in line.lower() for kw in GOLD_KEYWORDS)
        if has_numbers or has_tech:
            result.append(line)
    if not result:
        for line in lines:
            line = line.strip()
            if len(line) > 40:
                result.append(line)
            if len(result) >= 4:
                break
    return result[:6]


def _regex_tags(text: str) -> list:
    text_lower = text.lower()
    tag_map = {
        "n8n": "n8n", "make.com": "make.com", "zapier": "zapier",
        "claude": "Claude", "chatgpt": "ChatGPT", "gemini": "Gemini",
        "langchain": "LangChain", "rag": "RAG", "агент": "AI-агент",
        "автоматизаци": "автоматизация", "bitrix": "Bitrix24",
        "amocrm": "amoCRM", "python": "Python", "api": "API",
        "промпт": "промпт", "workflow": "workflow",
    }
    return [v for k, v in tag_map.items() if k in text_lower][:5]


# --- Сохранение GOLD ---

def save_gold(video_id: str, video: dict, text: str, category: str) -> str:
    extracted = extract_with_claude(text, video["title"])

    if extracted:
        main_idea      = extracted.get("main_idea", "_Не определена_")
        use_case       = extracted.get("use_case", "_Не описан_")
        workflow       = extracted.get("workflow", [])
        tech_stack     = extracted.get("tech_stack", [])
        tech_links     = extracted.get("tech_links", [])
        config_details = extracted.get("config_details", [])
        key_insights   = extracted.get("key_insights", [])
        gotchas        = extracted.get("gotchas", [])
        tags           = extracted.get("tags", [])
        mode = "Claude Haiku"
    else:
        main_idea      = _regex_main_idea(text)
        use_case       = "_Не описан_"
        workflow       = [_regex_schema(text)]
        tech_stack     = _regex_tech_links(text)
        tech_links     = _regex_tech_links(text)
        config_details = []
        key_insights   = _regex_meat(text)
        gotchas        = []
        tags           = _regex_tags(text)
        mode = "regex"

    def fmt_list(items: list, fallback: str = "_Нет данных_") -> str:
        return "\n".join(f"- {i}" for i in items) if items else fallback

    def fmt_steps(items: list) -> str:
        if not items:
            return "_Не описан_"
        return "\n".join(f"{n}. {s}" for n, s in enumerate(items, 1))

    tags_str = ", ".join(tags)
    target_dir = GOLD_CRM_DIR if category == "GOLD_CRM" else GOLD_TOOLS_DIR

    content = f"""---
source: YouTube / {video['channel']}
date: {video['date']}
original: {video['url']}
category: {category}
tags: [{tags_str}]
extracted_by: {mode}
---

## Суть
{main_idea}

## Бизнес-сценарий
{use_case}

## Алгоритм реализации
{fmt_steps(workflow)}

## Технический стек
{fmt_list(tech_stack)}

## Связки инструментов
{fmt_list(tech_links)}

## Конфигурация и параметры
{fmt_list(config_details)}

## Ключевые инсайты
{fmt_list(key_insights)}

## Подводные камни
{fmt_list(gotchas, "_Не упомянуты_")}
"""
    (target_dir / f"yt_{video_id}.md").write_text(content, encoding="utf-8")
    return mode


# --- Main ---

def main():
    if _claude:
        print("YT Processor запущен (режим: Claude Haiku)")
    else:
        print("YT Processor запущен (режим: regex — задай ANTHROPIC_API_KEY для Claude)")

    videos = parse_raw_dir()

    if not videos:
        print("Нет видео со status: raw в 00_RAW/YouTube/")
        return

    print(f"Новых для обработки: {len(videos)}\n")

    gold_crm_count = 0
    gold_tools_count = 0
    trash_count = 0
    processed_ids = []

    for i, video in enumerate(videos, 1):
        vid = video["video_id"]
        print(f"  [{i}/{len(videos)}] {video['title'][:65]}...")

        transcript = fetch_transcript(vid)
        time.sleep(3)
        full_text = " ".join(filter(None, [video["title"], video["description"], transcript])) or video["title"]

        category = classify(full_text)

        if category == "GOLD_CRM":
            mode = save_gold(vid, video, full_text, "GOLD_CRM")
            update_raw_file(video["filepath"], video["content"], "gold_crm", transcript)
            gold_crm_count += 1
            print(f"    ✅ GOLD_CRM [{mode}]  →  01_INBOX/Gold/yt_{vid}.md")
        elif category == "GOLD_TOOLS":
            mode = save_gold(vid, video, full_text, "GOLD_TOOLS")
            update_raw_file(video["filepath"], video["content"], "gold_tools", transcript)
            gold_tools_count += 1
            print(f"    🔧 GOLD_TOOLS [{mode}]  →  01_INBOX/Gold_Tools/yt_{vid}.md")
        else:
            update_raw_file(video["filepath"], video["content"], "trash", transcript)
            trash_count += 1
            print(f"    🗑️  TRASH")

        processed_ids.append(f"yt_{vid}")

    if processed_ids:
        update_processed_log(processed_ids)

    print(f"\nГотово: GOLD_CRM={gold_crm_count} | GOLD_TOOLS={gold_tools_count} | TRASH={trash_count}")
    print(f"📁 CRM: {GOLD_CRM_DIR}")
    print(f"🔧 Tools: {GOLD_TOOLS_DIR}")


if __name__ == "__main__":
    main()
