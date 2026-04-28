import os
import requests
from pathlib import Path

API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")

BASE_DIR = Path(__file__).parent.parent.parent
RAW_YT_DIR = BASE_DIR / "00_RAW" / "YouTube"
RAW_YT_DIR.mkdir(parents=True, exist_ok=True)

QUERIES = [
    "автоматизация бизнеса n8n 2026",
    "интеграция ИИ в Битрикс24 кейс",
    "настройка Claude API для amoCRM",
    "n8n workflow crm integration tutorial",
    "ИИ агенты для отдела продаж n8n",
    "автоматизация 1С через n8n",
    "make.com automation crm 2026",
    "ai agent workflow automation 2026",
]


def search_youtube():
    if not API_KEY or API_KEY == "YOUR_API_KEY":
        print("Ошибка: задайте YOUTUBE_API_KEY в переменных окружения.")
        return

    new_count = 0
    skip_count = 0
    base_url = "https://www.googleapis.com/youtube/v3/search"

    for query in QUERIES:
        print(f"Поиск: {query}")
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 10,
            "order": "date",
            "relevanceLanguage": "ru",
            "key": API_KEY,
        }

        try:
            res = requests.get(base_url, params=params, timeout=15)
            data = res.json()

            if "error" in data:
                print(f"  API ошибка: {data['error']['message']}")
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
                print(f"  + {title[:70]}")

        except Exception as e:
            print(f"  Ошибка '{query}': {e}")

    print(f"\nГотово: новых={new_count} | пропущено (уже есть)={skip_count}")
    print(f"Папка: {RAW_YT_DIR}")


if __name__ == "__main__":
    search_youtube()
