import os
import json
import time
import requests
from datetime import date
from pathlib import Path

# Script: infra_discovery.py (v2.0)
# Purpose: Deep discovery of AI solutions for business automation and role replacement.
# Output: 00_RAW/Infra/YYYY-MM-DD_infra_raw.json
# Pipeline: infra_discovery.py → infra_processor.py (Claude passports)
# IMPORTANT: Does NOT modify existing scripts (parser.py, processor.py, youtube_parser.py).

API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "00_RAW" / "Infra"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ─── 60 хирургических запросов ──────────────────────────────────────────────

QUERIES = [
    # === Мультиагентная инфраструктура ===
    "LangGraph multi-agent system business 2026",
    "CrewAI n8n business process automation tutorial",
    "Self-hosted LLM small business setup guide",
    "Ollama Docker deployment team server 2026",
    "vLLM high-load production deployment guide",
    "LangGraph n8n бизнес логика схема кейс",
    "автономный ИИ-агент Docker архитектура 2026",
    "RAG система локальные данные компании настройка",
    "vector database Chroma Weaviate бизнес кейс",
    "private GPT company knowledge base n8n",

    # === Замена менеджера по продажам ===
    "AI sales manager automation n8n CRM 2026",
    "нейросеть замена менеджера по продажам кейс",
    "AI квалификатор лидов автоматизация Bitrix24",
    "автоматические продажи ИИ-агент воронка n8n",
    "AI обработка входящих заявок CRM автоматизация",

    # === Замена ассистента / секретаря ===
    "AI assistant business automation n8n make.com",
    "ИИ ассистент замена секретаря автоматизация задач",
    "голосовой ИИ-ассистент бизнес n8n Telegram 2026",
    "AI executive assistant workflow automation Claude",
    "автоматизация рутинных задач ИИ ассистент кейс",

    # === Замена маркетолога ===
    "AI маркетолог контент автоматизация n8n 2026",
    "нейросеть замена контент-менеджера производство постов",
    "AI content marketing automation Claude n8n pipeline",
    "автоматическая генерация контента бизнес кейс ROI",
    "AI SMM менеджер автоматизация Telegram Instagram",

    # === Замена логиста ===
    "AI логистика автоматизация маршрутов n8n 2026",
    "ИИ замена логиста диспетчера кейс внедрение",
    "автоматизация заказов поставок ИИ 1С Bitrix24",
    "AI supply chain automation small business guide",
    "нейросеть планирование поставок склад автоматизация",

    # === Замена разработчика ===
    "Claude Code замена разработчика автоматизация кода",
    "AI разработчик без программиста n8n no-code 2026",
    "Cursor AI coding assistant replace developer guide",
    "AI code generation business automation ROI кейс",
    "GitHub Copilot замена junior разработчика кейс",

    # === Замена бухгалтера ===
    "AI бухгалтер автоматизация 1С n8n кейс 2026",
    "нейросеть замена бухгалтера документооборот",
    "автоматизация финансовой отчетности ИИ интеграция",
    "AI accounting automation small business ROI",
    "ИИ проверка счетов актов закрывающих документов",

    # === Замена юриста ===
    "AI юрист проверка договоров автоматизация 2026",
    "нейросеть замена юриста анализ документов кейс",
    "AI legal document review automation n8n Claude",
    "автоматическая проверка договоров ИИ бизнес",
    "ИИ юридическая экспертиза документов малый бизнес",

    # === Замена РОП / РОМ / HR ===
    "AI РОП мониторинг отдела продаж автоматизация",
    "ИИ контроль менеджеров продаж Bitrix24 n8n кейс",
    "AI HR рекрутер автоматизация найма сотрудников",
    "нейросеть проверка резюме онбординг автоматизация",
    "AI маркетинг директор управление кампаниями автоматизация",

    # === Замена отделов целиком ===
    "автоматизация отдела продаж ИИ полностью кейс",
    "замена колл-центра ИИ чатбот ROI 2026",
    "автоматизация отдела маркетинга ИИ агенты n8n",
    "ИИ замена IT отдела поддержки автоматизация",
    "полная автоматизация малого бизнеса ИИ кейс Россия",

    # === ROI и экономика внедрения ===
    "ROI внедрение ИИ бизнес расчет окупаемость",
    "сколько стоит ИИ агент разработка внедрение 2026",
    "экономия от ИИ замена сотрудника кейс реальный",
    "окупаемость автоматизации ИИ малый бизнес Россия",
    "бюджет на ИИ внедрение стартап малый бизнес план",
]

# ─── Поиск YouTube ───────────────────────────────────────────────────────────

def search_youtube(query: str, api_key: str, max_results: int = 5) -> list:
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "order": "relevance",
        "key": api_key,
    }
    try:
        r = requests.get(url, params=params, timeout=10).json()
        items = []
        for item in r.get("items", []):
            snippet = item["snippet"]
            items.append({
                "query": query,
                "title": snippet.get("title", ""),
                "channel": snippet.get("channelTitle", ""),
                "description": snippet.get("description", "")[:500],
                "link": f"https://youtube.com/watch?v={item['id']['videoId']}",
                "date": snippet.get("publishTime", "")[:10],
            })
        return items
    except Exception as e:
        print(f"  ⚠️  Ошибка '{query}': {e}")
        return []


# ─── Основная логика ─────────────────────────────────────────────────────────

def run():
    if API_KEY == "YOUR_API_KEY":
        print("❌ Укажите YOUTUBE_API_KEY в переменных окружения.")
        return

    today = date.today().strftime("%Y-%m-%d")
    json_path = RAW_DIR / f"{today}_infra_raw.json"
    md_path = RAW_DIR / f"{today}_infra_raw.md"

    all_results = []

    for i, query in enumerate(QUERIES, 1):
        print(f"[{i}/{len(QUERIES)}] Поиск: {query}")
        results = search_youtube(query, API_KEY)
        all_results.extend(results)
        print(f"  → Найдено: {len(results)} видео")
        time.sleep(1)

    # Дедупликация по ссылке
    seen = set()
    unique = []
    for item in all_results:
        if item["link"] not in seen:
            seen.add(item["link"])
            unique.append(item)

    # Сохранение JSON (для infra_processor.py)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)

    # Быстрый Markdown-дайджест для Obsidian
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 🔍 Infra Discovery Raw — {today}\n\n")
        f.write(f"**Запросов:** {len(QUERIES)} | **Найдено (уник.):** {len(unique)}\n\n")
        f.write("---\n\n")
        for item in unique:
            f.write(f"### [{item['title']}]({item['link']})\n")
            f.write(f"**Канал:** {item['channel']} | **Дата:** {item['date']}\n\n")
            f.write(f"> {item['description'][:200]}...\n\n")
            f.write(f"*Запрос: `{item['query']}`*\n\n---\n\n")

    print(f"\n✅ Готово: {len(unique)} уникальных видео")
    print(f"📄 JSON: {json_path}")
    print(f"📄 MD:   {md_path}")
    print(f"\n👉 Следующий шаг: запустить infra_processor.py для генерации паспортов идей")


if __name__ == "__main__":
    run()
