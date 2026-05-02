import os
import requests
from pathlib import Path
from datetime import datetime, timedelta, timezone

API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")
# Искать видео не старше N дней (0 = без ограничения)
DAYS_BACK = int(os.environ.get("YT_DAYS_BACK", "30"))

BASE_DIR = Path(__file__).parent.parent.parent
RAW_YT_DIR = BASE_DIR / "00_RAW" / "YouTube"
RAW_YT_DIR.mkdir(parents=True, exist_ok=True)

# ── GOLD_CRM — бизнес-автоматизация, CRM-интеграции ───────────────────────────
QUERIES_CRM = [
    "автоматизация бизнеса n8n 2026",
    "интеграция ИИ в Битрикс24 кейс",
    "настройка Claude API для amoCRM",
    "n8n workflow crm integration tutorial",
    "ИИ агенты для отдела продаж n8n",
    "автоматизация 1С через n8n",
    "make.com automation crm 2026",
    "ai agent workflow automation 2026",
    "ИИ автоматизация продаж кейс",
    "n8n телеграм бот crm интеграция",
]

# ── GOLD_TOOLS — инструменты, платформы, новые модели ─────────────────────────
QUERIES_TOOLS = [
    "vibe coding tutorial 2026",
    "вайбкодинг cursor windsurf 2026",
    "LangGraph multi-agent workflow tutorial",
    "CrewAI AutoGen мультиагентная система",
    "DeepSeek R2 обзор 2026",
    "Claude claude-sonnet-4-6 новые возможности",
    "GPT-5 обзор возможности 2026",
    "self-hosted LLM ollama llama deploy",
    "Dify Flowise self-hosted ai platform",
    "cursor ai ide coding tutorial 2026",
]

QUERIES = QUERIES_CRM + QUERIES_TOOLS


def search_youtube():
    if not API_KEY or API_KEY == "YOUR_API_KEY":
        print("Ошибка: задайте YOUTUBE_API_KEY в переменных окружения.")
        return

    published_after = None
    if DAYS_BACK > 0:
        dt = datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)
        published_after = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    new_count = 0
    skip_count = 0
    base_url = "https://www.googleapis.com/youtube/v3/search"

    crm_label = f"[CRM×{len(QUERIES_CRM)}]"
    tools_label = f"[TOOLS×{len(QUERIES_TOOLS)}]"
    date_label = f"последние {DAYS_BACK} дней" if DAYS_BACK else "без ограничения по дате"
    print(f"YT Discovery: {crm_label} {tools_label} | {date_label}\n")

    for query in QUERIES:
        tag = "CRM  " if query in QUERIES_CRM else "TOOLS"
        print(f"  [{tag}] {query}")
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 10,
            "order": "date",
            "relevanceLanguage": "ru",
            "key": API_KEY,
        }
        if published_after:
            params["publishedAfter"] = published_after

        try:
            res = requests.get(base_url, params=params, timeout=15)
            data = res.json()

            if "error" in data:
                print(f"    API ошибка: {data['error']['message']}")
                continue

            for item in data.get("items", []):
                video_id = item["id"].get("videoId")
                if not video_id:
                    continue

                filepath = RAW_YT_DIR / f"yt_{video_id}.md"
                if filepath.exists():
                    skip_count += 1
                    continue

                title = item["snippet"]["title"]
                channel = item["snippet"]["channelTitle"]
                pub_date = item["snippet"]["publishTime"][:10]
                url = f"https://youtube.com/watch?v={video_id}"
                description = item["snippet"].get("description", "").replace("\n", " ").strip()

                content = f"""---
video_id: {video_id}
title: {title}
channel: {channel}
date: {pub_date}
url: {url}
status: raw
---

## Описание
{description}
"""
                filepath.write_text(content, encoding="utf-8")
                new_count += 1
                print(f"    + {title[:70]}")

        except Exception as e:
            print(f"    Ошибка '{query}': {e}")

    print(f"\nГотово: новых={new_count} | пропущено (уже есть)={skip_count}")
    print(f"Папка: {RAW_YT_DIR}")


if __name__ == "__main__":
    search_youtube()
