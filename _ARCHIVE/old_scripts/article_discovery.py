import os
import sys
import requests

FIRE_API_KEY = os.environ.get("FIRECRAWL_API_KEY")
if not FIRE_API_KEY:
    print("Ошибка: переменная окружения FIRECRAWL_API_KEY не задана.")
    sys.exit(1)

TAGS = ["n8n", "CRM", "Low-code", "API", "Bitrix24", "amoCRM", "Python", "Автоматизация"]
PLATFORMS = ["habr.com", "vc.ru"]

def scrape_articles():
    raw_folder = "../../00_RAW/Articles"
    os.makedirs(raw_folder, exist_ok=True)

    for platform in PLATFORMS:
        for tag in TAGS:
            print(f"Скрапинг {platform} по тегу: {tag}")
            search_url = f"https://{platform}/search/?q={tag}"
            
            payload = {
                "url": search_url,
                "formats": ["markdown"],
                "onlyMainContent": True
            }
            headers = {
                "Authorization": f"Bearer {FIRE_API_KEY}",
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.post("https://api.firecrawl.dev/v1/scrape", json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    content = data.get("data", {}).get("markdown", "")
                    
                    filename = f"{platform.split('.')[0]}_{tag}.md"
                    with open(os.path.join(raw_folder, filename), "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f" Сохранено: {filename}")
                else:
                    print(f" Ошибка Firecrawl: {response.status_code}")
            except Exception as e:
                print(f" Ошибка при обработке {tag}: {e}")

if __name__ == '__main__':
    scrape_articles()
