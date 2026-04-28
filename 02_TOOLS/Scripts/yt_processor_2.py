import re
import os
import json
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
    _claude = anthropic_lib.Anthropic() if os.environ.get('ANTHROPIC_API_KEY') else None
except ImportError:
    _claude = None

_yt_api = YouTubeTranscriptApi()

BASE_DIR = Path(__file__).parent.parent.parent
REPORT_PATH = Path(__file__).parent / 'yt_discovery_report.md'
GOLD_DIR = BASE_DIR / '01_INBOX' / 'Gold'
PROCESSED_LOG = BASE_DIR / '01_INBOX' / 'processed_log.md'

GOLD_DIR.mkdir(parents=True, exist_ok=True)

GOLD_KEYWORDS = [
    'n8n', 'make.com', 'zapier', 'workflow', 'автоматизация', 'автоматизировать',
    'claude', 'chatgpt', 'gpt-', 'openai', 'anthropic', 'gemini', 'llm', 'llama',
    'агент', 'agent', 'prompt', 'промпт', 'api', 'интеграция', 'интегратор',
    'bitrix', 'amocrm', 'retailcrm', '1с', 'crm',
    'кейс', 'схема', 'гайд', 'инструкция', 'пошагово', 'туториал',
    'python', 'langchain', 'rag', 'vector', 'embeddings',
    'claude code', 'obsidian', 'notion', 'второй мозг',
    'нейросет', 'нейронн', 'модель', 'релиз',
]

TRASH_KEYWORDS = [
    'крипт', 'биткоин', 'токен', 'nft', 'майнинг', 'трейдинг',
    'заработок', 'заработай', 'пассивный доход', 'доход от',
    'похудей', 'похудение', 'диет', 'астролог', 'гадани',
    'ретрит', 'медитаци', 'эзотерик', 'нейрографик',
    'подработка', 'казино', 'ставки', 'форекс',
    'скидка', 'акция', 'промокод', 'реклама',
]

TOOLS = [
    'n8n', 'make.com', 'zapier', 'telegram', 'whatsapp', 'notion', 'obsidian',
    'claude', 'chatgpt', 'gpt', 'gemini', 'openai', 'anthropic',
    'bitrix24', 'amocrm', 'retailcrm', '1с', 'python', 'langchain',
    'api', 'webhook', 'http', 'rest', 'graphql',
    'google sheets', 'airtable', 'postgresql', 'mysql', 'redis',
    'docker', 'vps', 'server', 'github',
]

CLAUDE_SYSTEM = """Ты — эксперт по автоматизации бизнеса, ИИ-инструментам и CRM-системам.
Анализируй контент YouTube-видео об автоматизации и извлекай структурированную практическую информацию.
Отвечай строго на русском языке, кратко и по делу."""

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "main_idea": {
            "type": "string",
            "description": "Главная практическая мысль видео — 1-2 предложения"
        },
        "workflow": {
            "type": "string",
            "description": "Пошаговая схема автоматизации или workflow. Формат: шаг1 → шаг2 → шаг3. Если схемы нет — '_Не описана_'"
        },
        "tech_links": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Технические связки инструментов. Пример: ['n8n → Bitrix24', 'Claude API → CRM']. Пустой массив если нет"
        },
        "key_insights": {
            "type": "array",
            "items": {"type": "string"},
            "description": "3-5 ключевых практических выводов — конкретные факты, цифры, приёмы"
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Теги из списка: n8n, make.com, zapier, Claude, ChatGPT, Gemini, LangChain, RAG, AI-агент, автоматизация, Bitrix24, amoCRM, Python, API, workflow"
        }
    },
    "required": ["main_idea", "workflow", "tech_links", "key_insights", "tags"],
    "additionalProperties": False
}


def load_processed_ids():
    if not PROCESSED_LOG.exists():
        return set()
    content = PROCESSED_LOG.read_text(encoding='utf-8')
    return set(re.findall(r'\b(yt_[a-zA-Z0-9_-]+)\b', content))


def update_processed_log(new_ids: list):
    today = date.today().strftime('%Y-%m-%d')
    entry = f"\n### YouTube ({len(new_ids)} видео) — {today}\n"
    entry += ', '.join(new_ids) + '\n'
    with open(PROCESSED_LOG, 'a', encoding='utf-8') as f:
        f.write(entry)


def parse_report(report_path: Path) -> list[dict]:
    videos = []
    content = report_path.read_text(encoding='utf-8')
    pattern = r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*\[Смотреть\]\((https://youtube\.com/watch\?v=([a-zA-Z0-9_-]+))\)\s*\|'
    for m in re.finditer(pattern, content):
        videos.append({
            'channel': m.group(1).strip(),
            'title': m.group(2).strip(),
            'date': m.group(3).strip(),
            'url': m.group(4).strip(),
            'video_id': m.group(5).strip(),
        })
    return videos


def fetch_transcript(video_id: str) -> str:
    try:
        transcript = _yt_api.fetch(video_id, languages=['ru', 'en'])
        return ' '.join(entry.text for entry in transcript)
    except RequestBlocked:
        print("  ⚠️  YouTube блокирует запросы с этого IP (облачный сервер).")
        print("     Запусти скрипт локально на своём компьютере.")
        return ''
    except (NoTranscriptFound, TranscriptsDisabled):
        return ''
    except Exception as e:
        print(f"  Ошибка транскрипта {video_id}: {e}")
        return ''


def classify(text: str) -> str:
    text_lower = text.lower()
    trash_score = sum(1 for kw in TRASH_KEYWORDS if kw in text_lower)
    gold_score = sum(1 for kw in GOLD_KEYWORDS if kw in text_lower)
    if trash_score >= 2:
        return 'TRASH'
    if gold_score >= 2:
        return 'GOLD'
    if gold_score == 1 and trash_score == 0:
        return 'GOLD'
    return 'TRASH'


# --- Извлечение через Claude API ---

def extract_with_claude(text: str, title: str) -> dict | None:
    """Извлекает структурированную информацию через Claude Haiku."""
    if not _claude:
        return None

    # Ограничиваем транскрипт до ~6000 слов чтобы уложиться в контекст и бюджет
    content = text[:12000] if len(text) > 12000 else text

    user_prompt = f"Заголовок видео: {title}\n\nТранскрипт:\n{content}"

    try:
        response = _claude.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system=[{
                "type": "text",
                "text": CLAUDE_SYSTEM,
                "cache_control": {"type": "ephemeral"}  # кэшируем системный промпт
            }],
            messages=[{"role": "user", "content": user_prompt}],
            output_config={
                "format": {
                    "type": "json_schema",
                    "schema": EXTRACTION_SCHEMA
                }
            }
        )
        raw = next((b.text for b in response.content if b.type == "text"), "{}")
        result = json.loads(raw)

        # Логируем стоимость (кэш-хиты снижают цену)
        usage = response.usage
        cached = getattr(usage, 'cache_read_input_tokens', 0)
        if cached:
            print(f"    💾 Кэш: {cached} токенов сэкономлено")

        return result

    except Exception as e:
        print(f"    ⚠️  Claude API ошибка: {e}")
        return None


# --- Fallback: извлечение через regex (если нет API ключа) ---

def _regex_main_idea(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    return sentences[0] if sentences else text[:200]


def _regex_schema(text: str) -> str:
    lines = text.split('\n')
    schema_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(m in line for m in ['→', '->', '➡', '⟶', '▶']):
            schema_lines.append(line)
        elif re.match(r'^\d+[\.\)]\s', line):
            schema_lines.append(line)
        elif any(w in line.lower() for w in ['шаг', 'сначала', 'затем', 'потом', 'далее']):
            schema_lines.append(line)
    return '\n'.join(schema_lines[:8]) if schema_lines else '_Не описана_'


def _regex_tech_links(text: str) -> list:
    text_lower = text.lower()
    found = [t for t in TOOLS if t in text_lower]
    if len(found) < 2:
        return found
    links = []
    for sentence in re.split(r'[.!?\n]', text_lower):
        tools_in = [t for t in found if t in sentence]
        if len(tools_in) >= 2:
            link = ' → '.join(tools_in[:3])
            if link not in links:
                links.append(link)
    return links[:5] if links else found[:4]


def _regex_meat(text: str) -> list:
    lines = text.split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if len(line) < 20:
            continue
        has_numbers = bool(re.search(r'\d+[%\+\-×xX]|\d{4,}|\d+\s*(руб|тыс|млн|мин|час|сек)', line))
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
        'n8n': 'n8n', 'make.com': 'make.com', 'zapier': 'zapier',
        'claude': 'Claude', 'chatgpt': 'ChatGPT', 'gemini': 'Gemini',
        'langchain': 'LangChain', 'rag': 'RAG', 'агент': 'AI-агент',
        'автоматизаци': 'автоматизация', 'bitrix': 'Bitrix24',
        'amocrm': 'amoCRM', 'python': 'Python', 'api': 'API',
        'промпт': 'промпт', 'workflow': 'workflow',
    }
    return [v for k, v in tag_map.items() if k in text_lower][:5]


# --- Сохранение ---

def save_gold(video_id: str, video: dict, text: str):
    filename = f"yt_{video_id}"

    # Пробуем Claude API
    extracted = extract_with_claude(text, video['title'])

    if extracted:
        main_idea = extracted.get('main_idea', '_Не определена_')
        schema = extracted.get('workflow', '_Не описана_')
        tech_links = extracted.get('tech_links', [])
        key_insights = extracted.get('key_insights', [])
        tags = extracted.get('tags', [])
        mode = 'Claude Haiku'
    else:
        # Fallback: regex
        main_idea = _regex_main_idea(text)
        schema = _regex_schema(text)
        tech_links = _regex_tech_links(text)
        key_insights = _regex_meat(text)
        tags = _regex_tags(text)
        mode = 'regex'

    tech_links_str = '\n'.join(f'- {t}' for t in tech_links) if tech_links else '_Не найдены_'
    insights_str = '\n'.join(f'- {i}' for i in key_insights) if key_insights else '_Нет данных_'
    tags_str = ', '.join(tags)

    content = f"""---
source: YouTube / {video['channel']}
date: {video['date']}
original: {video['url']}
category: GOLD
tags: [{tags_str}]
extracted_by: {mode}
---

## Главная мысль
{main_idea}

## Схема / Workflow
{schema}

## Технические связки
{tech_links_str}

## Мясо
{insights_str}
"""
    (GOLD_DIR / f"{filename}.md").write_text(content, encoding='utf-8')
    return mode


def main():
    if _claude:
        print("🤖 YT Processor 2 запущен (режим: Claude Haiku)")
    else:
        print("🔧 YT Processor 2 запущен (режим: regex — установи ANTHROPIC_API_KEY для Claude)")

    if not REPORT_PATH.exists():
        print(f"Файл не найден: {REPORT_PATH}")
        return

    videos = parse_report(REPORT_PATH)
    if not videos:
        print("Видео в отчёте не найдены.")
        return

    processed = load_processed_ids()
    new_videos = [v for v in videos if f"yt_{v['video_id']}" not in processed]

    print(f"📂 Всего: {len(videos)} | Новых: {len(new_videos)}\n")

    if not new_videos:
        print("✅ Нет новых видео.")
        return

    gold_count = 0
    trash_count = 0
    processed_ids = []

    for i, video in enumerate(new_videos, 1):
        vid = video['video_id']
        label = f"yt_{vid}"
        print(f"  [{i}/{len(new_videos)}] {video['title'][:60]}...")

        text = fetch_transcript(vid)

        if not text or len(text) < 50:
            text = video['title']

        category = classify(text)

        if category == 'GOLD':
            mode = save_gold(vid, video, text)
            gold_count += 1
            print(f"    ✅ GOLD [{mode}]")
        else:
            trash_count += 1
            print(f"    🗑️  TRASH")

        processed_ids.append(label)

    if processed_ids:
        update_processed_log(processed_ids)

    print(f"\n✅ Готово: GOLD={gold_count} | TRASH={trash_count}")
    print(f"📁 Результат: {GOLD_DIR}")


if __name__ == '__main__':
    main()
