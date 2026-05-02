import os
import json
import time
from datetime import date
from pathlib import Path
import anthropic

# Script: infra_processor.py (v1.0)
# Purpose: Read raw infra discoveries → Claude API → Idea Passports (Паспорт идеи).
# Input:  00_RAW/Infra/YYYY-MM-DD_infra_raw.json
# Output:
#   ИТОГ ≥22  → 05_BIZ_RECIPES/083_infra_<slug>.md
#   ИТОГ 18–21 → 08_IDEAS_LAB/08.2_SELECTED/infra_<slug>.md
#   ИТОГ <18  → 08_IDEAS_LAB/08.1_RAW_IDEAS/infra_<slug>.md
#   Digest    → 01_INBOX/Gold/infra_digest_YYYY-MM-DD.md
# IMPORTANT: Does NOT modify any existing scripts or their output folders.

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "00_RAW" / "Infra"
BIZ_RECIPES_DIR = BASE_DIR / "05_BIZ_RECIPES"
SELECTED_DIR = BASE_DIR / "08_IDEAS_LAB" / "08.2_SELECTED"
RAW_IDEAS_DIR = BASE_DIR / "08_IDEAS_LAB" / "08.1_RAW_IDEAS"
GOLD_DIR = BASE_DIR / "01_INBOX" / "Gold"

for d in [SELECTED_DIR, RAW_IDEAS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ─── Счётчик BIZ_RECIPES ────────────────────────────────────────────────────

def next_recipe_number() -> int:
    existing = sorted(BIZ_RECIPES_DIR.glob("0*.md"))
    if not existing:
        return 83
    last = existing[-1].stem.split("_")[0]
    try:
        return int(last) + 1
    except ValueError:
        return 83

# ─── Промпт для Claude ──────────────────────────────────────────────────────

SYSTEM_PROMPT = """Ты — эксперт по автоматизации бизнеса на основе ИИ.
Студия Трофимов — интегратор ИИ и CRM (Bitrix24, amoCRM, n8n, Make.com, Claude).
Твоя задача: анализировать материал о ИИ-решениях и генерировать готовые «Паспорта идей»
для основателя студии — Максима Трофимова.

Принципы оценки:
- Pain (1–10): насколько острая боль у клиента. 9–10 = массово, дорого стоит вручную.
- Dev (1–10): сложность реализации. 1 = легко за неделю, 10 = полгода команды.
- Profit (1–10): потенциал выручки для Студии. 10 = можно продавать за 300к+.
- ИТОГ = Pain + Dev (инверсия: 10-Dev) + Profit. Максимум 30.
  Формула: Pain + (10 - Dev) + Profit

Целевая аудитория Студии: малый и средний бизнес в России,
бюджет проекта 50 000 – 500 000 руб., хотят автоматизировать процессы и сократить персонал."""

PASSPORT_PROMPT = """Проанализируй это YouTube-видео об ИИ и автоматизации бизнеса.

**Видео:**
Название: {title}
Канал: {channel}
Описание: {description}
Запрос, по которому найдено: {query}

Сгенерируй «Паспорт идеи» строго в формате ниже. Пиши конкретно, без воды.
Если видео не содержит практической бизнес-ценности — верни JSON со score=0.

Ответ ТОЛЬКО в JSON:
{{
  "name": "Краткое название идеи (3-6 слов)",
  "category": "Замена должности | Автоматизация отдела | Инфраструктура | ROI/Экономика",
  "replaces": "Конкретная должность или отдел, которые заменяет. Если не применимо — null",
  "what_it_gives": "2-3 предложения: конкретная польза для клиента Студии Трофимов",
  "pros": ["плюс 1", "плюс 2", "плюс 3"],
  "cons": ["минус/риск 1", "минус/риск 2"],
  "cost": {{
    "development": "Стоимость разработки для Студии, например '40 000 – 80 000 руб.'",
    "infrastructure": "Инфраструктура клиента в месяц, например '5 000 – 15 000 руб./мес'",
    "support": "Поддержка/доработки в месяц"
  }},
  "price_for_client": "Сколько можно продать клиенту, например '120 000 – 200 000 руб.'",
  "artifacts": {{
    "tools": ["инструмент 1", "инструмент 2"],
    "repos": ["GitHub ссылка или название репо, если известно"],
    "apis": ["API 1", "API 2"],
    "docs": ["ссылка или название документации"]
  }},
  "steps": ["Шаг 1", "Шаг 2", "Шаг 3", "Шаг 4"],
  "studio_revenue_potential": "Оценка выручки Студии за 6 мес если сделать продукт",
  "pain": 7,
  "dev": 5,
  "profit": 8,
  "score": 20,
  "verdict": "Одно предложение: стоит ли брать в работу и почему"
}}"""

# ─── Вызов Claude ────────────────────────────────────────────────────────────

def generate_passport(client: anthropic.Anthropic, item: dict) -> dict | None:
    prompt = PASSPORT_PROMPT.format(
        title=item["title"],
        channel=item["channel"],
        description=item.get("description", "")[:400],
        query=item["query"],
    )
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        # Извлекаем JSON из ответа
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ⚠️  JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"  ⚠️  Claude error: {e}")
        return None

# ─── Формирование Markdown паспорта ─────────────────────────────────────────

def render_passport(item: dict, passport: dict, today: str) -> str:
    cost = passport.get("cost", {})
    artifacts = passport.get("artifacts", {})
    pros = "\n".join(f"- {p}" for p in passport.get("pros", []))
    cons = "\n".join(f"- {c}" for c in passport.get("cons", []))
    steps = "\n".join(f"{i+1}. {s}" for i, s in enumerate(passport.get("steps", [])))
    tools = ", ".join(artifacts.get("tools", [])) or "—"
    repos = "\n".join(f"- {r}" for r in artifacts.get("repos", [])) or "- —"
    apis = ", ".join(artifacts.get("apis", [])) or "—"
    docs = "\n".join(f"- {d}" for d in artifacts.get("docs", [])) or "- —"

    pain = passport.get("pain", 0)
    dev = passport.get("dev", 0)
    profit = passport.get("profit", 0)
    score = passport.get("score", pain + (10 - dev) + profit)

    return f"""---
date: {today}
source: YouTube
original: {item["link"]}
category: INFRA_DISCOVERY
replaces: {passport.get("replaces") or "—"}
score: Pain={pain} Dev={dev} Profit={profit} ИТОГ={score}
tags: [{passport.get("category", "")}, {tools}]
---

# 🗂️ Паспорт идеи: {passport.get("name", item["title"])}

**Источник:** [{item["title"]}]({item["link"]}) — {item["channel"]} ({item["date"]})
**Категория:** {passport.get("category", "—")}
**Заменяет:** {passport.get("replaces") or "—"}

---

## 💡 Что это даёт бизнесу
{passport.get("what_it_gives", "—")}

---

## ✅ Плюсы
{pros}

## ❌ Минусы / Риски
{cons}

---

## 💰 Экономика

| Параметр | Значение |
|---|---|
| Стоимость разработки | {cost.get("development", "—")} |
| Инфраструктура/мес | {cost.get("infrastructure", "—")} |
| Поддержка/мес | {cost.get("support", "—")} |
| **Цена для клиента** | **{passport.get("price_for_client", "—")}** |
| Потенциал выручки Студии | {passport.get("studio_revenue_potential", "—")} |

---

## 🧰 Артефакты для реализации

**Инструменты:** {tools}
**API:** {apis}

**Репозитории:**
{repos}

**Документация:**
{docs}

---

## 🚀 Шаги запуска
{steps}

---

## 📊 Demand Matrix
| Pain | Dev | Profit | **ИТОГ** |
|:---:|:---:|:---:|:---:|
| {pain} | {dev} | {profit} | **{score}** |

**Вердикт:** {passport.get("verdict", "—")}
"""

# ─── Slug из названия ────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    import re
    text = text.lower()
    text = re.sub(r"[^a-zа-яё0-9\s]", "", text)
    text = re.sub(r"\s+", "_", text.strip())
    return text[:40]

# ─── Дайджест ────────────────────────────────────────────────────────────────

def render_digest(results: list, today: str) -> str:
    top = [r for r in results if r["score"] >= 22]
    mid = [r for r in results if 18 <= r["score"] < 22]

    lines = [f"# 🏭 Infra Discovery Digest — {today}\n"]
    lines.append(f"**Обработано:** {len(results)} | **PROJECT (≥22):** {len(top)} | **IDEAS_LAB (18–21):** {len(mid)}\n")
    lines.append("---\n")

    if top:
        lines.append("## 🔴 В ПРОИЗВОДСТВО (≥22)\n")
        for r in top:
            lines.append(f"- **[{r['name']}]({r['link']})** — ИТОГ={r['score']} | {r['replaces'] or r['category']}")
            lines.append(f"  > {r['verdict']}\n")

    if mid:
        lines.append("## 🟠 В IDEAS_LAB (18–21)\n")
        for r in mid:
            lines.append(f"- **[{r['name']}]({r['link']})** — ИТОГ={r['score']} | {r['replaces'] or r['category']}")
            lines.append(f"  > {r['verdict']}\n")

    return "\n".join(lines)

# ─── Основная логика ─────────────────────────────────────────────────────────

def run():
    if not ANTHROPIC_API_KEY:
        print("❌ Укажите ANTHROPIC_API_KEY в переменных окружения.")
        return

    # Берём последний JSON из 00_RAW/Infra/
    json_files = sorted(RAW_DIR.glob("*_infra_raw.json"), reverse=True)
    if not json_files:
        print("❌ Нет файлов в 00_RAW/Infra/. Сначала запустите infra_discovery.py")
        return

    json_path = json_files[0]
    print(f"📂 Читаю: {json_path.name}")

    with open(json_path, encoding="utf-8") as f:
        items = json.load(f)

    print(f"📋 Найдено видео: {len(items)}\n")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    today = date.today().strftime("%Y-%m-%d")
    recipe_num = next_recipe_number()

    digest_rows = []
    counts = {"biz_recipe": 0, "selected": 0, "raw": 0, "skip": 0}

    for i, item in enumerate(items, 1):
        print(f"[{i}/{len(items)}] {item['title'][:60]}...")

        passport = generate_passport(client, item)

        if not passport or passport.get("score", 0) == 0:
            print(f"  ⚫ Пропуск (нет ценности)")
            counts["skip"] += 1
            time.sleep(0.5)
            continue

        score = passport.get("score", 0)
        name = passport.get("name", item["title"])
        slug = slugify(name)
        content = render_passport(item, passport, today)

        if score >= 22:
            filename = f"{recipe_num:03d}_infra_{slug}.md"
            (BIZ_RECIPES_DIR / filename).write_text(content, encoding="utf-8")
            print(f"  🔴 BIZ_RECIPE [{score}] → {filename}")
            recipe_num += 1
            counts["biz_recipe"] += 1
        elif score >= 18:
            filename = f"infra_{slug}_{today}.md"
            (SELECTED_DIR / filename).write_text(content, encoding="utf-8")
            print(f"  🟠 SELECTED [{score}] → {filename}")
            counts["selected"] += 1
        else:
            filename = f"infra_{slug}_{today}.md"
            (RAW_IDEAS_DIR / filename).write_text(content, encoding="utf-8")
            print(f"  🟡 RAW_IDEA [{score}] → {filename}")
            counts["raw"] += 1

        digest_rows.append({
            "name": name,
            "link": item["link"],
            "score": score,
            "category": passport.get("category", ""),
            "replaces": passport.get("replaces"),
            "verdict": passport.get("verdict", ""),
        })

        time.sleep(1)

    # Сохранение дайджеста
    digest_content = render_digest(digest_rows, today)
    digest_path = GOLD_DIR / f"infra_digest_{today}.md"
    digest_path.write_text(digest_content, encoding="utf-8")

    print(f"\n✅ Готово!")
    print(f"  🔴 BIZ_RECIPES: {counts['biz_recipe']}")
    print(f"  🟠 SELECTED:    {counts['selected']}")
    print(f"  🟡 RAW_IDEAS:   {counts['raw']}")
    print(f"  ⚫ Пропущено:   {counts['skip']}")
    print(f"\n📄 Дайджест: {digest_path}")


if __name__ == "__main__":
    run()
