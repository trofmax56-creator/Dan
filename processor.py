import re
from pathlib import Path
from datetime import date

# Пути
BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / '00_RAW' / 'Telegram'
GOLD_DIR = BASE_DIR / '01_INBOX' / 'Gold'           # → gold_synthesizer (продукты CRM)
GOLD_TOOLS_DIR = BASE_DIR / '01_INBOX' / 'Gold_Tools'  # → справочник инструментов
PROCESSED_LOG = BASE_DIR / '01_INBOX' / 'processed_log.md'

GOLD_DIR.mkdir(parents=True, exist_ok=True)
GOLD_TOOLS_DIR.mkdir(parents=True, exist_ok=True)

# ── GOLD_CRM — контент для синтеза продуктов (→ gold_synthesizer) ────────────
GOLD_CRM_KEYWORDS = [
    'n8n', 'make.com', 'zapier', 'workflow', 'автоматизация', 'автоматизировать',
    'bitrix', 'amocrm', 'retailcrm', '1с', 'crm', 'интеграция', 'интегратор',
    'api', 'webhook',
    'агент', 'agent', 'prompt', 'промпт',
    'claude', 'chatgpt', 'gpt-', 'openai', 'anthropic', 'gemini', 'llm',
    'нейросет', 'нейронн', 'модель', 'релиз',
    'python', 'langchain', 'rag', 'vector', 'embeddings',
    'кейс', 'схема', 'гайд', 'инструкция', 'пошагово', 'туториал',
    'obsidian', 'notion', 'второй мозг',
    'аналитик', 'дашборд', 'визуализаци', 'метрик',
]

# ── GOLD_TOOLS — инструменты, платформы, вайбкодинг (→ Gold_Tools, не в synthesizer) ─
GOLD_TOOLS_KEYWORDS = [
    # Мультиагентные системы
    'мультиагент', 'multiagent', 'multi-agent', 'агентная архитектур',
    'langgraph', 'crewai', 'autogen', 'оркестратор',
    'hermes agent', 'hermes',

    # Vibe coding и AI-IDE
    'вайбкодинг', 'vibecoding', 'vibe coding', 'vibe-coding',
    'cursor', 'windsurf', 'bolt', 'lovable', 'replit', 'claude code', 'copilot',

    # Новые AI-платформы
    'emergent', 'same.dev', 'v0.dev', 'vercel ai', 'atoms',
    'dify', 'flowise', 'langflow',
    'omi', 'open clow', 'openrouter', 'perplexity', 'antigravity',

    # Установка и деплой
    'деплой', 'deploy', 'self-hosted', 'установка', 'настройк', 'docker compose',

    # Модели нового поколения
    'deepseek', 'mistral', 'qwen', 'llama', 'ollama', 'sonnet', 'opus', 'gpt-5',
    'gemma',

    # Контент и публикации
    'контент', 'публикаци', 'постинг',
]

# ── Ключевые CRM-якоря (если есть — всегда Gold, не Tools) ───────────────────
CRM_ANCHORS = ['bitrix', 'amocrm', 'retailcrm', 'crm', 'n8n', 'make.com', 'webhook', 'интеграц']

# TRASH — мусор, не берём
TRASH_KEYWORDS = [
    'крипт', 'биткоин', 'токен', 'nft', 'майнинг', 'трейдинг',
    'заработок', 'заработай', 'пассивный доход', 'доход от',
    'похудей', 'похудение', 'диет', 'астролог', 'гадани',
    'ретрит', 'медитаци', 'эзотерик', 'нейрографик',
    'подработка', 'казино', 'ставки', 'форекс',
    'скидка', 'акция', 'промокод', 'реклама',
]

# Инструменты для поиска технических связок
TOOLS = [
    'n8n', 'make.com', 'zapier', 'telegram', 'whatsapp', 'notion', 'obsidian',
    'claude', 'chatgpt', 'gpt', 'gemini', 'openai', 'anthropic',
    'bitrix24', 'amocrm', 'retailcrm', '1с', 'python', 'langchain',
    'api', 'webhook', 'http', 'rest', 'graphql',
    'google sheets', 'airtable', 'postgresql', 'mysql', 'redis',
    'docker', 'vps', 'server', 'github',
    # Новые инструменты
    'langgraph', 'crewai', 'autogen', 'cursor', 'windsurf', 'bolt', 'lovable',
    'emergent', 'dify', 'flowise', 'langflow', 'replit', 'vercel',
    'deepseek', 'mistral', 'llama', 'ollama',
    'openrouter', 'perplexity', 'hermes', 'omi', 'gemma', 'antigravity',
]


def load_processed_files():
    if not PROCESSED_LOG.exists():
        return set()
    content = PROCESSED_LOG.read_text(encoding='utf-8')
    return set(re.findall(r'\b([a-zA-Z0-9_]+_\d+)\b', content))


def update_processed_log(new_files: list):
    today = date.today().strftime('%Y-%m-%d')
    entry = f"\n### Telegram ({len(new_files)} файлов) — {today}\n"
    entry += ', '.join(new_files) + '\n'
    with open(PROCESSED_LOG, 'a', encoding='utf-8') as f:
        f.write(entry)


def parse_raw_file(filepath: Path):
    content = filepath.read_text(encoding='utf-8')
    date_match = re.search(r'date:\s*(.+)', content)
    link_match = re.search(r'link:\s*(.+)', content)
    parts = content.split('---')
    text = parts[-1].strip() if len(parts) >= 3 else content
    date_str = date_match.group(1).strip()[:10] if date_match else ''
    link = link_match.group(1).strip() if link_match else ''
    return text, date_str, link


def classify(text: str) -> str:
    """Возвращает: GOLD_CRM | GOLD_TOOLS | TRASH"""
    text_lower = text.lower()
    trash_score = sum(1 for kw in TRASH_KEYWORDS if kw in text_lower)
    if trash_score >= 2:
        return 'TRASH'

    crm_score = sum(1 for kw in GOLD_CRM_KEYWORDS if kw in text_lower)
    tools_score = sum(1 for kw in GOLD_TOOLS_KEYWORDS if kw in text_lower)
    has_crm_anchor = any(a in text_lower for a in CRM_ANCHORS)

    # CRM-якорь всегда побеждает — идёт в gold_synthesizer
    if has_crm_anchor and crm_score >= 1:
        return 'GOLD_CRM'
    if crm_score >= 2:
        return 'GOLD_CRM'
    if tools_score >= 2:
        return 'GOLD_TOOLS'
    if tools_score == 1 and trash_score == 0:
        return 'GOLD_TOOLS'
    if crm_score == 1 and trash_score == 0:
        return 'GOLD_CRM'
    return 'TRASH'


def extract_main_idea(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    return sentences[0] if sentences else text[:200]


def extract_schema(text: str) -> str:
    lines = text.split('\n')
    schema_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Строки со стрелками, шагами, нумерацией
        if any(marker in line for marker in ['→', '->', '➡', '⟶', '▶']):
            schema_lines.append(line)
        elif re.match(r'^\d+[\.\)]\s', line):
            schema_lines.append(line)
        elif any(w in line.lower() for w in ['шаг', 'сначала', 'затем', 'потом', 'далее', 'после этого']):
            schema_lines.append(line)
    return '\n'.join(schema_lines[:8]) if schema_lines else '_Не описана_'


def extract_tech_links(text: str) -> list:
    text_lower = text.lower()
    found_tools = [t for t in TOOLS if t in text_lower]
    if len(found_tools) < 2:
        return found_tools

    links = []
    # Ищем пары инструментов в одном предложении
    sentences = re.split(r'[.!?\n]', text_lower)
    for sentence in sentences:
        tools_in_sentence = [t for t in found_tools if t in sentence]
        if len(tools_in_sentence) >= 2:
            link = ' → '.join(tools_in_sentence[:3])
            if link not in links:
                links.append(link)
    return links[:5] if links else [t for t in found_tools[:4]]


def extract_meat(text: str) -> str:
    lines = text.split('\n')
    meat_lines = []
    for line in lines:
        line = line.strip()
        if len(line) < 20:
            continue
        # Строки с числами, процентами, конкретными данными
        has_numbers = bool(re.search(r'\d+[%\+\-×xX]|\d{4,}|\d+\s*(руб|тыс|млн|мин|час|сек)', line))
        has_tech = any(kw in line.lower() for kw in GOLD_CRM_KEYWORDS + GOLD_TOOLS_KEYWORDS)
        if has_numbers or has_tech:
            meat_lines.append(f"- {line}")
    if not meat_lines:
        # Если ничего не нашли — берём первые содержательные строки
        for line in lines:
            line = line.strip()
            if len(line) > 40:
                meat_lines.append(f"- {line}")
            if len(meat_lines) >= 4:
                break
    return '\n'.join(meat_lines[:6])


def extract_tags(text: str) -> list:
    text_lower = text.lower()
    tag_map = {
        'n8n': 'n8n', 'make.com': 'make.com', 'zapier': 'zapier',
        'claude': 'Claude', 'chatgpt': 'ChatGPT', 'gemini': 'Gemini',
        'langchain': 'LangChain', 'rag': 'RAG', 'агент': 'AI-агент',
        'автоматизаци': 'автоматизация', 'bitrix': 'Bitrix24',
        'amocrm': 'amoCRM', 'python': 'Python', 'api': 'API',
        'промпт': 'промпт', 'workflow': 'workflow',
        # Новые теги
        'мультиагент': 'мультиагент', 'langgraph': 'LangGraph',
        'crewai': 'CrewAI', 'autogen': 'AutoGen',
        'вайбкодинг': 'вайбкодинг', 'vibecoding': 'вайбкодинг',
        'cursor': 'Cursor', 'windsurf': 'Windsurf', 'bolt': 'Bolt',
        'emergent': 'Emergent', 'dify': 'Dify', 'flowise': 'Flowise',
        'deepseek': 'DeepSeek', 'ollama': 'Ollama',
        'аналитик': 'аналитика', 'дашборд': 'дашборд',
        'деплой': 'деплой', 'self-hosted': 'self-hosted',
    }
    return [v for k, v in tag_map.items() if k in text_lower][:5]


def save_gold(filename: str, text: str, date_str: str, link: str, channel: str, target_dir: Path = None):
    main_idea = extract_main_idea(text)
    schema = extract_schema(text)
    tech_links = extract_tech_links(text)
    meat = extract_meat(text)
    tags = extract_tags(text)

    tech_links_str = '\n'.join(f'- {t}' for t in tech_links) or '_Не найдены_'
    tags_str = ', '.join(tags)

    content = f"""---
source: @{channel}
date: {date_str}
original: {link}
category: GOLD
tags: [{tags_str}]
---

## Главная мысль
{main_idea}

## Схема / Workflow
{schema}

## Технические связки
{tech_links_str}

## Мясо
{meat}
"""
    out_dir = target_dir if target_dir else GOLD_DIR
    (out_dir / f"{filename}.md").write_text(content, encoding='utf-8')


def main():
    print("🤖 Processor (keyword mode) запущен...")

    processed = load_processed_files()
    raw_files = sorted(RAW_DIR.glob('*.md'))
    new_files = [f for f in raw_files if f.stem not in processed]

    print(f"📂 Всего: {len(raw_files)} | Новых: {len(new_files)}\n")

    if not new_files:
        print("✅ Нет новых файлов.")
        return

    gold_crm_count = 0
    gold_tools_count = 0
    trash_count = 0
    processed_names = []

    for i, filepath in enumerate(new_files, 1):
        filename = filepath.stem
        channel = filename.rsplit('_', 1)[0]

        try:
            text, date_str, link = parse_raw_file(filepath)
            if len(text) < 50:
                trash_count += 1
                processed_names.append(filename)
                continue

            category = classify(text)

            if category == 'GOLD_CRM':
                save_gold(filename, text, date_str, link, channel, GOLD_DIR)
                gold_crm_count += 1
                tags = ', '.join(extract_tags(text))
                print(f"  ✅ GOLD_CRM [{i}/{len(new_files)}] {filename} | {tags}")
            elif category == 'GOLD_TOOLS':
                save_gold(filename, text, date_str, link, channel, GOLD_TOOLS_DIR)
                gold_tools_count += 1
                tags = ', '.join(extract_tags(text))
                print(f"  🔧 GOLD_TOOLS [{i}/{len(new_files)}] {filename} | {tags}")
            else:
                trash_count += 1
                print(f"  🗑️  TRASH [{i}/{len(new_files)}] {filename}")

            processed_names.append(filename)

        except Exception as e:
            print(f"  ❌ [{filename}]: {e}")

    if processed_names:
        update_processed_log(processed_names)

    print(f"\n✅ Готово: GOLD_CRM={gold_crm_count} | GOLD_TOOLS={gold_tools_count} | TRASH={trash_count}")
    print(f"📁 CRM: {GOLD_DIR}")
    print(f"🔧 Tools: {GOLD_TOOLS_DIR}")


if __name__ == '__main__':
    main()
