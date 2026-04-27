import os
import requests
import json

# Для работы требуется API_KEY от Google Cloud Console (YouTube Data API v3)
API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")

QUERIES = [
    "автоматизация бизнеса n8n 2026",
    "интеграция ИИ в Битрикс24 кейс",
    "настройка Claude API для amoCRM",
    "n8n workflow crm integration tutorial",
    "ИИ агенты для отдела продаж n8n",
    "автоматизация 1С через n8n"
]

TECHNICAL_KEYWORDS = ["настройка", "схема", "tutorial", "кейс", "workflow", "инструкция", "код"]

def search_youtube():
    if API_KEY == "YOUR_API_KEY":
        print("Ошибка: Укажите YOUTUBE_API_KEY в переменных окружения.")
        return

    discovered_videos = []
    base_url = "https://www.googleapis.com/youtube/v3/search"

    for query in QUERIES:
        print(f"Поиск YouTube: {query}")
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 10,
            "order": "date",
            "relevanceLanguage": "ru",
            "key": API_KEY
        }
        
        try:
            res = requests.get(base_url, params=params)
            data = res.json()
            
            if "items" in data:
                for item in data["items"]:
                    title = item["snippet"]["title"]
                    desc = item["snippet"]["description"]
                    
                    content_to_check = (title + " " + desc).lower()
                    if any(word in content_to_check for word in TECHNICAL_KEYWORDS):
                        discovered_videos.append({
                            "title": title,
                            "channel": item["snippet"]["channelTitle"],
                            "channelId": item["snippet"]["channelId"],
                            "link": f"https://youtube.com/watch?v={item['id']['videoId']}",
                            "date": item["snippet"]["publishTime"][:10]
                        })
        except Exception as e:
            print(f" Ошибка поиска '{query}': {e}")

    output_path = 'yt_discovery_report.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 📽️ Результаты глубокой разведки YouTube\n\n")
        f.write("| Канал | Видео | Дата | Ссылка |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for v in discovered_videos:
            f.write(f"| {v['channel']} | {v['title']} | {v['date']} | [Смотреть]({v['link']}) |\n")
            
    print(f"Разведка YouTube завершена. Найдено видео: {len(discovered_videos)}")

if __name__ == '__main__':
    search_youtube()
