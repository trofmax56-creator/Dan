import os
import re
import xml.etree.ElementTree as ET
import requests

channels = [
    {'name': 'ivanbekunai', 'id': 'UCZ5mD7nE4jA8n3-u4Wv5hVg'},
    {'name': 'nickvels_ai', 'id': 'UCuTX807i8wvA'},
    {'name': 'igorzuevich', 'id': 'UCNheTD-hN-Es'},
    {'name': 'sukhov_live', 'id': 'UCbgzOjVtKskI'},
    {'name': 'yevgeniykovalenko', 'id': 'UCOlnRKsVZ58'},
    {'name': 'serejaris', 'id': 'UCi49d_NnXAOI'},
    {'name': 'neuropros', 'id': 'UCrcDsMsU_W9Q'},
    {'name': 'rixaihub', 'id': 'UCFzgZg_ghsf0'},
    {'name': 'rinatsuleyman', 'id': 'UCg0VGNfTtMtA'},
    {'name': 'aikirichenkoy', 'id': 'UC5xeRaCykWbw'}
]

# Автоматическое определение папки
base_dir = os.path.dirname(os.path.abspath(__file__))
raw_folder = os.path.join(base_dir, '00_RAW', 'YouTube')
os.makedirs(raw_folder, exist_ok=True)

def get_latest_videos_rss():
    for channel in channels:
        try:
            print(f"Парсинг YouTube (через RSS): {channel['name']}")
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel['id']}"
            response = requests.get(rss_url, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                # Берем последние 2 видео
                entries = root.findall('{http://www.w3.org/2005/Atom}entry')[:2]
                
                for entry in entries:
                    title = entry.find('{http://www.w3.org/2005/Atom}title').text
                    video_id = entry.find('{http://www.youtube.com/xml/schemas/2015}videoId').text
                    
                    filename = f"{video_id}.md"
                    full_path = os.path.join(raw_folder, filename)
                    
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(f"---\ntitle: {title}\nlink: https://youtube.com/watch?v={video_id}\n---\n\n{title}")
            else:
                print(f"Ошибка доступа к RSS: {response.status_code}")
        except Exception as e:
            print(f"Ошибка в канале {channel['name']}: {e}")

if __name__ == '__main__':
    get_latest_videos_rss()
