import os
import json
import asyncio
import re
from pathlib import Path
import anthropic

# Пути
BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / '00_RAW' / 'Telegram'
GOLD_DIR = BASE_DIR / '01_INBOX' / 'Gold'
PROCESSED_LOG = BASE_DIR / '01_INBOX' / 'processed_log.md'

GOLD_DIR.mkdir(parents=True, exist_ok=True)

# Claude клиент
client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

SYSTEM_PROMPT = """Ты — старший контент-менеджер AI/автоматизация проекта Brief AI Agent.

Твоя задача — анализировать Telegram-посты и выносить вердикт GOLD или TRASH.

GOLD — если пост содержит РЕАЛЬНУЮ ПРАКТИКУ:
- AI+CRM связки, n8n/Make схемы с конкретными шагами
- Кейсы внедрения с результатами (%, рубли, часы)
- Новые AI-модели (Claude, GPT, Gemini) с техническими данными
- Гайды по автоматизации, workflow-схемы
- Claude Code, n8n, Make.com — практические примеры
- Prompt engineering с реальными примерами промптов

TRASH — если пост содержит:
- Новости без практики («вышла модель X» без деталей)
- Мотивацию, лайфстайл, личные истории без техники
- Рекламу курсов без конкретного контента
- Общие рассуждения об ИИ без инструкций
- Крипта, заработок, инвестиции

Отвечай СТРОГО в JSON без markdown-блоков:
{
  "category": "GOLD" или "TRASH",
  "main_idea": "Главная мысль в 1-2 предложениях (только для GOLD, иначе null)",
  "schema": "Схема/workflow если есть — опиши шаги или инструменты (только для GOLD, иначе null)",
  "tech_links": ["Tool1 → Tool2", "Claude API → n8n → Telegram"] (только для GOLD, иначе []),
  "meat": "Ключевые практические инсайты — конкретные факты, цифры, шаги (только для GOLD, иначе null)",
  "tags": ["n8n", "Claude", "автоматизация"] (3-5 тегов, только для GOLD, иначе [])
}"""


def load_processed_files():
    """Читает processed_log.md и возвращает set уже обработанных файлов."""
    processed = set()
    if not PROCESSED_LOG.exists():
        return processed
    content = PROCESSED_LOG.read_text(encoding='utf-8')
    # Ищем имена файлов в формате channelname_id
    matches = re.findall(r'\b([a-zA-Z0-9_]+_\d+)\b', content)
    processed.update(matches)
    return processed


def update_processed_log(new_files: list):
    """Добавляет новые файлы в processed_log.md."""
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')

    entry = f"\n### Telegram ({len(new_files)} файлов) — {today}\n"
    entry += ', '.join(new_files) + '\n'

    with open(PROCESSED_LOG, 'a', encoding='utf-8') as f:
        f.write(entry)


def classify_post(text: str, source_info: str) -> dict:
    """Вызывает Claude API для классификации поста."""
    response = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                'role': 'user',
                'content': f"Источник: {source_info}\n\nТекст поста:\n{text[:3000]}"
            }
        ]
    )
    raw = response.content[0].text.strip()
    # Убираем markdown-блоки если модель всё же добавила
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    return json.loads(raw)


def save_gold(filename: str, result: dict, source_info: str, original_link: str, date_str: str):
    """Сохраняет GOLD пост в 01_INBOX/Gold/."""
    channel = filename.rsplit('_', 1)[0]
    tags = ', '.join(result.get('tags', []))
    tech_links = '\n'.join(f'- {t}' for t in result.get('tech_links', []))

    content = f"""---
source: @{channel}
date: {date_str}
original: {original_link}
category: GOLD
tags: [{tags}]
---

## Главная мысль
{result.get('main_idea', '')}

## Схема / Workflow
{result.get('schema') or '_Не описана_'}

## Технические связки
{tech_links or '_Не указаны_'}

## Мясо
{result.get('meat', '')}
"""
    out_path = GOLD_DIR / f"{filename}.md"
    out_path.write_text(content, encoding='utf-8')


def parse_raw_file(filepath: Path):
    """Читает .md файл из 00_RAW и извлекает метаданные."""
    content = filepath.read_text(encoding='utf-8')
    date_match = re.search(r'date:\s*(.+)', content)
    link_match = re.search(r'link:\s*(.+)', content)
    # Текст поста — всё после второго ---
    parts = content.split('---')
    text = parts[-1].strip() if len(parts) >= 3 else content

    date_str = date_match.group(1).strip() if date_match else ''
    link = link_match.group(1).strip() if link_match else ''
    return text, date_str, link


def main():
    print("🤖 Processor запущен...")

    processed = load_processed_files()
    raw_files = sorted(RAW_DIR.glob('*.md'))
    new_files = [f for f in raw_files if f.stem not in processed]

    print(f"📂 Всего файлов: {len(raw_files)} | Новых для обработки: {len(new_files)}\n")

    if not new_files:
        print("✅ Нет новых файлов для обработки.")
        return

    gold_count = 0
    trash_count = 0
    processed_names = []
    errors = []

    for i, filepath in enumerate(new_files, 1):
        filename = filepath.stem
        channel = filename.rsplit('_', 1)[0]

        try:
            text, date_str, link = parse_raw_file(filepath)
            if len(text) < 50:
                trash_count += 1
                processed_names.append(filename)
                continue

            result = classify_post(text, f"@{channel} | {link}")

            if result['category'] == 'GOLD':
                save_gold(filename, result, f"@{channel}", link, date_str)
                gold_count += 1
                tags = ', '.join(result.get('tags', []))
                print(f"  ✅ GOLD [{i}/{len(new_files)}] {filename} | {tags}")
            else:
                trash_count += 1
                print(f"  🗑️  TRASH [{i}/{len(new_files)}] {filename}")

            processed_names.append(filename)

        except json.JSONDecodeError as e:
            errors.append(filename)
            print(f"  ⚠️  JSON error [{filename}]: {e}")
        except Exception as e:
            errors.append(filename)
            print(f"  ❌ Error [{filename}]: {e}")

        # Пауза чтобы не упереться в rate limit
        if i % 10 == 0:
            import time
            time.sleep(1)

    if processed_names:
        update_processed_log(processed_names)

    print(f"\n✅ Готово: GOLD={gold_count} | TRASH={trash_count} | Ошибок={len(errors)}")
    print(f"📁 Gold файлы: {GOLD_DIR}")
    if errors:
        print(f"⚠️  Ошибки: {', '.join(errors)}")


if __name__ == '__main__':
    main()
