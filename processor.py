import re
from pathlib import Path
from datetime import date

# Пути
BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / '00_RAW' / 'Telegram'
GOLD_DIR = BASE_DIR / '01_INBOX' / 'Gold'
PROCESSED_LOG = BASE_DIR / '01_INBOX' / 'processed_log.md'

GOLD_DIR.mkdir(parents=True, exist_ok=True)

# GOLD — практический AI/автоматизация контент
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
        has_tech = any(kw in line.lower() for kw in GOLD_KEYWORDS)
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
    }
    return [v for k, v in tag_map.items() if k in text_lower][:5]


def save_gold(filename: str, text: str, date_str: str, link: str, channel: str):
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
    (GOLD_DIR / f"{filename}.md").write_text(content, encoding='utf-8')


def main():
    print("🤖 Processor (keyword mode) запущен...")

    processed = load_processed_files()
    raw_files = sorted(RAW_DIR.glob('*.md'))
    new_files = [f for f in raw_files if f.stem not in processed]

    print(f"📂 Всего: {len(raw_files)} | Новых: {len(new_files)}\n")

    if not new_files:
        print("✅ Нет новых файлов.")
        return

    gold_count = 0
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

            if category == 'GOLD':
                save_gold(filename, text, date_str, link, channel)
                gold_count += 1
                tags = ', '.join(extract_tags(text))
                print(f"  ✅ GOLD [{i}/{len(new_files)}] {filename} | {tags}")
            else:
                trash_count += 1
                print(f"  🗑️  TRASH [{i}/{len(new_files)}] {filename}")

            processed_names.append(filename)

        except Exception as e:
            print(f"  ❌ [{filename}]: {e}")

    if processed_names:
        update_processed_log(processed_names)

    print(f"\n✅ Готово: GOLD={gold_count} | TRASH={trash_count}")
    print(f"📁 Результат: {GOLD_DIR}")


if __name__ == '__main__':
    main()
