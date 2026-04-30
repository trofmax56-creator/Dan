import os
import json
import time
from datetime import date
from pathlib import Path
import anthropic

# Script: gold_synthesizer.py (v1.0)
# Purpose: Batch synthesis of Gold files → commercial AI products (vern_ideas format).
# Input:  01_INBOX/Gold/ — last N files (sorted by mtime)
# Output:
#   ИТОГ > 24 → 05_BIZ_RECIPES/
#   ИТОГ 20–24 → 08_IDEAS_LAB/08.2_SELECTED/
#   Digest    → 08_IDEAS_LAB/08.2_SELECTED/products_digest_YYYY-MM-DD.md
# IMPORTANT: Does NOT modify existing scripts.

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

BASE_DIR = Path(__file__).parent
GOLD_DIR = BASE_DIR / "01_INBOX" / "Gold"
BIZ_RECIPES_DIR = BASE_DIR / "05_BIZ_RECIPES"
SELECTED_DIR = BASE_DIR / "08_IDEAS_LAB" / "08.2_SELECTED"

SELECTED_DIR.mkdir(parents=True, exist_ok=True)

# Сколько Gold-файлов брать за один прогон
BATCH_SIZE = int(os.environ.get("GOLD_BATCH_SIZE", "40"))

# ─── Счётчик BIZ_RECIPES ────────────────────────────────────────────────────

def next_recipe_number() -> int:
    existing = sorted(BIZ_RECIPES_DIR.glob("0*.md"))
    if not existing:
        return 100
    last = existing[-1].stem.split("_")[0]
    try:
        return int(last) + 1
    except ValueError:
        return 100

# ─── Системный промпт (кешируется) ──────────────────────────────────────────

SYSTEM_PROMPT = """Ты — главный продуктовый архитектор Студии Трофимов (Россия).
Студия продаёт автоматизацию на ИИ малому и среднему бизнесу: n8n, Claude, Bitrix24, amoCRM, 1С, МойСклад, Wazzup.
Клиенты: МСБ России, бюджет 50 000–500 000 руб., хотят сократить ФОТ и автоматизировать процессы.

Правила:
- Адаптируй западные решения под РФ (ЮKassa, Wazzup, СберБизнес вместо западных аналогов)
- Бизнес-сценарий пиши живо — конкретная ситуация, диалог или кейс
- Цены только в рублях
- Demand Matrix: Pain + (10 − Dev) + Profit. Порог производства: ИТОГ > 24

Формат ответа — строго JSON-массив продуктов."""

# ─── Промпт синтеза ──────────────────────────────────────────────────────────

def build_prompt(gold_content: str) -> str:
    return f"""Проанализируй эти материалы из папки GOLD и синтезируй коммерческие ИИ-продукты для Студии Трофимов.

--- МАТЕРИАЛЫ GOLD ---
{gold_content}
--- КОНЕЦ МАТЕРИАЛОВ ---

Из этих материалов выдели идеи с ИТОГ > 18 и опиши каждую как готовый продукт.

Ответ — строго JSON-массив:
[
  {{
    "name": "AI-[Название]",
    "essence": "1-2 предложения — механика решения",
    "scenario": "Конкретная ситуация клиента — как будто ты описываешь реальный кейс",
    "logic": "Trigger → Process → Action",
    "stack": ["n8n", "Claude 3.5 Sonnet", "..."],
    "integrations": "Как сервисы соединены (n8n как оркестратор)",
    "algorithm": ["Шаг 1", "Шаг 2", "Шаг 3"],
    "why_buy": "Экономия ФОТ или деньги — конкретные цифры",
    "cost_dev": "Стоимость разработки, например '60 000 – 100 000 руб.'",
    "cost_infra": "Инфраструктура/мес, например '5 000 – 10 000 руб./мес'",
    "price_client": "Цена для клиента, например '150 000 – 250 000 руб.'",
    "source_files": ["filename1.md", "filename2.md"],
    "pain": 8,
    "dev": 4,
    "profit": 9,
    "score": 23,
    "verdict": "Одно предложение: стоит ли брать в работу"
  }}
]

Если идей нет — верни пустой массив [].
Минимум 3, максимум 10 продуктов за один прогон."""

# ─── Чтение Gold-файлов ──────────────────────────────────────────────────────

def load_gold_batch(batch_size: int) -> tuple[str, list[str]]:
    files = sorted(GOLD_DIR.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    files = files[:batch_size]

    chunks = []
    names = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8")[:800]
            chunks.append(f"=== {f.name} ===\n{content}")
            names.append(f.name)
        except Exception:
            pass

    return "\n\n".join(chunks), names

# ─── Рендер Markdown ─────────────────────────────────────────────────────────

def render_product(p: dict, today: str) -> str:
    stack = ", ".join(p.get("stack", []))
    algo = "\n".join(f"{i+1}. {s}" for i, s in enumerate(p.get("algorithm", [])))
    sources = ", ".join(f"[[{s}]]" for s in p.get("source_files", []))
    pain = p.get("pain", 0)
    dev = p.get("dev", 0)
    profit = p.get("profit", 0)
    score = p.get("score", pain + (10 - dev) + profit)

    return f"""---
date: {today}
source: Gold Synthesis
category: PRODUCT
score: Pain={pain} Dev={dev} Profit={profit} ИТОГ={score}
tags: [{stack}]
---

# 🚀 Продукт: {p.get("name", "—")}

**Суть:** {p.get("essence", "—")}

---

## 🎯 Бизнес-сценарий
{p.get("scenario", "—")}

## ⚙️ Логика
{p.get("logic", "—")}

## 🛠 Технический стек
{stack}

## 🔗 Связки инструментов
{p.get("integrations", "—")}

## 📋 Алгоритм реализации
{algo}

## 💰 Почему купят (ROI)
{p.get("why_buy", "—")}

## 💵 Экономика

| Параметр | Значение |
|---|---|
| Стоимость разработки | {p.get("cost_dev", "—")} |
| Инфраструктура/мес | {p.get("cost_infra", "—")} |
| **Цена для клиента** | **{p.get("price_client", "—")}** |

## 📊 Demand Matrix
| Pain | Dev | Profit | **ИТОГ** |
|:---:|:---:|:---:|:---:|
| {pain} | {dev} | {profit} | **{score}** |

**Вердикт:** {p.get("verdict", "—")}

## 📚 Источники
{sources}
"""

# ─── Slug ────────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    import re
    text = re.sub(r"[^a-zа-яё0-9\s]", "", text.lower())
    text = re.sub(r"\s+", "_", text.strip())
    return text[:40]

# ─── Дайджест ────────────────────────────────────────────────────────────────

def render_digest(products: list, today: str, source_files: list) -> str:
    top = [p for p in products if p["score"] > 24]
    mid = [p for p in products if 20 <= p["score"] <= 24]

    lines = [
        f"# 🏭 Gold Synthesizer — {today}\n",
        f"**Файлов обработано:** {len(source_files)} | **Продуктов:** {len(products)} | **В производство (>24):** {len(top)} | **Ideas Lab (20–24):** {len(mid)}\n",
        "---\n",
    ]
    if top:
        lines.append("## 🔴 В ПРОИЗВОДСТВО (>24)\n")
        for p in top:
            lines.append(f"- **{p['name']}** — ИТОГ={p['score']}")
            lines.append(f"  > {p['verdict']}\n")
    if mid:
        lines.append("## 🟠 IDEAS LAB (20–24)\n")
        for p in mid:
            lines.append(f"- **{p['name']}** — ИТОГ={p['score']}")
            lines.append(f"  > {p['verdict']}\n")
    return "\n".join(lines)

# ─── Основная логика ─────────────────────────────────────────────────────────

def run():
    if not ANTHROPIC_API_KEY:
        print("❌ Укажите ANTHROPIC_API_KEY в переменных окружения.")
        return

    today = date.today().strftime("%Y-%m-%d")
    print(f"📂 Читаю последние {BATCH_SIZE} файлов из Gold...")

    gold_content, source_files = load_gold_batch(BATCH_SIZE)

    if not source_files:
        print("❌ Gold-папка пуста.")
        return

    print(f"✅ Загружено: {len(source_files)} файлов")
    print("🤖 Отправляю в Claude для синтеза продуктов...\n")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": build_prompt(gold_content)}],
    )

    raw = response.content[0].text.strip()
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    try:
        products = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка парсинга JSON: {e}")
        print(raw[:500])
        return

    print(f"✅ Синтезировано продуктов: {len(products)}\n")

    recipe_num = next_recipe_number()
    counts = {"biz": 0, "selected": 0, "skip": 0}

    for p in products:
        score = p.get("score", 0)
        name = p.get("name", "unknown")
        slug = slugify(name)
        content = render_product(p, today)

        if score > 24:
            filename = f"{recipe_num:03d}_gold_{slug}.md"
            (BIZ_RECIPES_DIR / filename).write_text(content, encoding="utf-8")
            print(f"  🔴 BIZ_RECIPE [{score}] {name} → {filename}")
            recipe_num += 1
            counts["biz"] += 1
        elif score >= 20:
            filename = f"product_{slug}_{today}.md"
            (SELECTED_DIR / filename).write_text(content, encoding="utf-8")
            print(f"  🟠 SELECTED [{score}] {name}")
            counts["selected"] += 1
        else:
            print(f"  ⚫ Пропуск [{score}] {name}")
            counts["skip"] += 1

    # Дайджест
    digest = render_digest(products, today, source_files)
    digest_path = SELECTED_DIR / f"products_digest_{today}.md"
    digest_path.write_text(digest, encoding="utf-8")

    print(f"\n✅ Готово!")
    print(f"  🔴 BIZ_RECIPES: {counts['biz']}")
    print(f"  🟠 SELECTED:    {counts['selected']}")
    print(f"  ⚫ Пропущено:   {counts['skip']}")
    print(f"  📄 Дайджест:    {digest_path}")

if __name__ == "__main__":
    run()
