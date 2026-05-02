import os
import json
import time
from datetime import date
from pathlib import Path
import anthropic

# Script: gold_synthesizer.py (v2.0)
# Purpose: Batch synthesis of Gold files → commercial AI products (v3.0 standard).
# Input:  01_INBOX/Gold/ — last N files (sorted by mtime)
# Output:
#   ИТОГ > 24  → 05_BIZ_RECIPES/
#   ИТОГ 20–24 → 08_IDEAS_LAB/08.2_SELECTED/
#   ИТОГ 18–19 → 08_IDEAS_LAB/08.1_RAW_IDEAS/
#   Digest     → 08_IDEAS_LAB/08.2_SELECTED/products_digest_YYYY-MM-DD.md
# IMPORTANT: Does NOT modify existing scripts.

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

BASE_DIR = Path(__file__).parent
GOLD_DIR = BASE_DIR / "01_INBOX" / "Gold"
BIZ_RECIPES_DIR = BASE_DIR / "05_BIZ_RECIPES"
SELECTED_DIR = BASE_DIR / "08_IDEAS_LAB" / "08.2_SELECTED"
RAW_IDEAS_DIR = BASE_DIR / "08_IDEAS_LAB" / "08.1_RAW_IDEAS"

SELECTED_DIR.mkdir(parents=True, exist_ok=True)
RAW_IDEAS_DIR.mkdir(parents=True, exist_ok=True)

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

SYSTEM_PROMPT = """Ты — главный продуктовый архитектор Студии Трофимов (Россия). Стандарт продукта v3.0.
Студия продаёт автоматизацию на ИИ малому и среднему бизнесу: n8n, Claude, Bitrix24, amoCRM, 1С, МойСклад, Wazzup.
Клиенты: МСБ России, бюджет 50 000–500 000 руб., хотят сократить ФОТ и автоматизировать процессы.

═══ СТАНДАРТ ОПИСАНИЯ ПРОДУКТА v3.0 ═══

1. НАЗВАНИЕ: Формат строго «AI-[Роль]» + расшифровка в скобках.
   Имя = роль = что заменяет или улучшает. Клиент с первого слова понимает что покупает.
   ✓ Примеры: «AI-Сито» (Умный Квалификатор), «AI-Некромант» (Реаниматор базы), «AI-Ревизор» (Контроль 100% звонков).
   ✗ Нельзя: «AI-Sales Helper», «AI-Automation Tool», «AI-Менеджер».

2. СУТЬ: 1–2 предложения — только механика решения, без воды.

3. БИЗНЕС-СЦЕНАРИЙ: Живая сцена по формату «ДО → ИИ делает → клиент получает».
   Пиши конкретными словами, которые говорит клиент и что ИИ отвечает/делает.
   Клиент должен узнать себя, читая этот абзац.
   ✓ Можно: «Клиент пишет в WhatsApp: "Сколько стоит?" Менеджер занят. ИИ отвечает: "Привет! Подскажите, какая у вас ниша?" После ответов ИИ сам заполняет карточку в Битриксе.»
   ✗ Нельзя: «Система помогает автоматизировать процесс квалификации».

4. ЛОГИКА: Путь данных одной строкой через стрелки. Формат: Trigger → Process → Action.

5. ТЕХНИЧЕСКИЙ СТЕК: Только РФ-совместимые инструменты:
   Wazzup (не Twilio), ЮKassa (не Stripe), Dadata (не Clearbit), UIS/МТС Exolve (не Twilio Voice).

6. АЛГОРИТМ РЕАЛИЗАЦИИ: 3–5 шагов для n8n-инженера.
   Конкретные глаголы действия + числа где применимо.
   ✓ Можно: «Рассылка по 20 сообщений в час», «Уведомление РОПу при оценке < 3».
   ✗ Нельзя: «настроить интеграцию», «подключить API».

7. ПОЧЕМУ КУПЯТ (ROI): Формула = боль + цифра + крючок-инсайт.
   Боль: что теряет клиент прямо сейчас без этого продукта.
   Цифра: рубли, часы, проценты — обязательно конкретно.
   Крючок: одна фраза, которая запоминается и передаётся дальше.
   ✓ Можно: «Заменяет штат ОКК из 2 человек (160 000 руб./мес. ФОТ). Стоимость возврата клиента в 10 раз ниже нового лида.»
   ✗ Нельзя: «экономит время и повышает эффективность».

8. ЭКОНОМИКА: Разработка для Студии / инфраструктура клиента в месяц / цена продажи клиенту.

9. ИСТОЧНИК: Список исходных Gold-файлов.

═══ DEMAND MATRIX ═══
Pain + (10 − Dev) + Profit = ИТОГ (max 30).
ИТОГ > 24 → в производство | 20–24 → следующий спринт | 18–19 → идея (не срочно) | < 18 → пропуск.

Формат ответа — строго JSON-массив продуктов."""

# ─── Промпт синтеза ──────────────────────────────────────────────────────────

def build_prompt(gold_content: str) -> str:
    return f"""Проанализируй эти материалы из папки GOLD и синтезируй коммерческие ИИ-продукты для Студии Трофимов по стандарту v3.0.

--- МАТЕРИАЛЫ GOLD ---
{gold_content}
--- КОНЕЦ МАТЕРИАЛОВ ---

Из этих материалов выдели идеи с ИТОГ ≥ 18 и опиши каждую как готовый продукт.

СТРОГИЕ ТРЕБОВАНИЯ К ФОРМАТУ (стандарт v3.0):

"name": Формат «AI-[Роль]» + пробел + «(Расшифровка)». Имя = что заменяет.
  ✓ «AI-Сито (Умный Квалификатор)», «AI-Некромант (Реаниматор базы)»
  ✗ «AI-Helper», «AI-Sales Tool»

"scenario": Живая сцена «ДО → ИИ делает → клиент получает».
  Включи реальные слова клиента в кавычках. Клиент должен узнать себя.
  ✓ «Менеджер занят. Клиент пишет в WhatsApp: "Сколько стоит?" ИИ отвечает: "Привет! Подскажите нишу и кол-во сотрудников?" После ответов ИИ сам заполняет карточку в Битрикс24.»
  ✗ «Система автоматизирует процесс квалификации входящих лидов.»

"algorithm": Конкретные глаголы + числа где применимо.
  ✓ ["Настроить webhook в n8n на входящие WhatsApp-сообщения через Wazzup", "Claude извлекает 5 параметров квалификации из диалога", "Уведомление РОПу если скор < 3 из 5"]
  ✗ ["Настроить интеграцию", "Подключить API", "Протестировать"]

"why_buy": Формула боль + цифра + крючок-инсайт (запоминаемая фраза).
  ✓ «Менеджер тратит 40 мин на квалификацию одного лида вручную — 120 лидов/мес × 40 мин = 80 часов = 2 рабочие недели. AI-Сито делает это за 3 минуты. Крючок: "Менеджер продаёт, а не анкетирует."»
  ✗ «Экономит время и повышает конверсию.»

Ответ — строго JSON-массив:
[
  {{
    "name": "AI-[Роль] (Расшифровка)",
    "essence": "1-2 предложения — только механика, без воды",
    "scenario": "Живая сцена ДО → ИИ делает → клиент получает. Слова клиента в кавычках.",
    "logic": "Trigger → Process → Action (через стрелки, одна строка)",
    "stack": ["n8n", "claude-sonnet-4-6", "Wazzup", "Bitrix24"],
    "integrations": "Wazzup → n8n Webhook → Claude (квалификация) → Bitrix24 REST API",
    "algorithm": [
      "Шаг с глаголом + число/параметр",
      "Шаг с глаголом + число/параметр",
      "Шаг с глаголом + число/параметр"
    ],
    "why_buy": "Боль (что теряет сейчас) + цифра в рублях/часах + крючок-инсайт",
    "cost_dev": "40 000 – 80 000 руб.",
    "cost_infra": "3 000 – 7 000 руб./мес",
    "price_client": "80 000 – 150 000 руб. + 15 000 руб./мес поддержка",
    "source_files": ["filename1.md"],
    "pain": 8,
    "dev": 4,
    "profit": 9,
    "score": 25,
    "verdict": "Одно предложение: стоит ли брать в производство и почему"
  }}
]

Если идей нет — верни пустой массив [].
Минимум 3, максимум 10 продуктов за один прогон."""

# ─── Чтение Gold-файлов ──────────────────────────────────────────────────────

def load_gold_batch(batch_size: int) -> tuple[str, list[str]]:
    files = sorted(GOLD_DIR.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    files = [f for f in files if not f.name.startswith("infra_digest")]
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
    stack_list = p.get("stack", [])
    stack = "\n".join(f"- {s}" for s in stack_list)
    stack_tags = ", ".join(stack_list)
    algo = "\n".join(f"{i+1}. {s}" for i, s in enumerate(p.get("algorithm", [])))
    sources = "\n".join(f"- [[{s}]]" for s in p.get("source_files", []))
    pain = p.get("pain", 0)
    dev = p.get("dev", 0)
    profit = p.get("profit", 0)
    score = p.get("score", pain + (10 - dev) + profit)
    name = p.get("name", "—")
    slug_name = name.split("(")[0].strip() if "(" in name else name
    subtitle = name.split("(")[1].rstrip(")").strip() if "(" in name else ""

    return f"""---
title: {name}
date: {today}
source: Gold Synthesis v3.0
score: {score}
pain: {pain}
dev: {dev}
profit: {profit}
status: {"production" if score > 24 else "selected" if score >= 20 else "raw"}
tags: [{stack_tags}]
---

## 1. Название
**{slug_name}** — {subtitle}

## 2. Суть
{p.get("essence", "—")}

## 3. Бизнес-сценарий
{p.get("scenario", "—")}

## 4. Логика
```
{p.get("logic", "—")}
```

## 5. Технический стек
{stack}

## 6. Связки инструментов
```
{p.get("integrations", "—")}
```

## 7. Алгоритм реализации
{algo}

## 8. Почему купят (ROI)
{p.get("why_buy", "—")}

## 9. Экономика
| Статья | Сумма |
|---|---|
| Разработка для Студии | {p.get("cost_dev", "—")} |
| Инфраструктура клиента | {p.get("cost_infra", "—")} |
| Цена продажи клиенту | {p.get("price_client", "—")} |

---

**Demand Matrix:** Pain={pain} | Dev={dev} | Profit={profit} | **ИТОГ={score}**

**Вердикт:** {p.get("verdict", "—")}

## Источники
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
    raw = [p for p in products if 18 <= p["score"] < 20]

    lines = [
        f"# 🏭 Gold Synthesizer v3.0 — {today}\n",
        f"**Файлов:** {len(source_files)} | **Продуктов:** {len(products)} | **BIZ_RECIPES (>24):** {len(top)} | **SELECTED (20–24):** {len(mid)} | **RAW (18–19):** {len(raw)}\n",
        "---\n",
    ]
    if top:
        lines.append("## 🔴 В ПРОИЗВОДСТВО (>24)\n")
        for p in top:
            lines.append(f"- **{p['name']}** — ИТОГ={p['score']}")
            lines.append(f"  > {p['verdict']}\n")
    if mid:
        lines.append("## 🟠 SELECTED (20–24)\n")
        for p in mid:
            lines.append(f"- **{p['name']}** — ИТОГ={p['score']}")
            lines.append(f"  > {p['verdict']}\n")
    if raw:
        lines.append("## 🟡 RAW IDEAS (18–19)\n")
        for p in raw:
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
    counts = {"biz": 0, "selected": 0, "raw": 0, "skip": 0}

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
        elif score >= 18:
            filename = f"raw_{slug}_{today}.md"
            (RAW_IDEAS_DIR / filename).write_text(content, encoding="utf-8")
            print(f"  🟡 RAW_IDEAS [{score}] {name}")
            counts["raw"] += 1
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
    print(f"  🟡 RAW_IDEAS:   {counts['raw']}")
    print(f"  ⚫ Пропущено:   {counts['skip']}")
    print(f"  📄 Дайджест:    {digest_path}")

if __name__ == "__main__":
    run()
