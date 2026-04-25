import os
import xml.etree.ElementTree as ET
import requests

# Список каналов с проверенными ID (UC...)
channels = [
    {'name': 'ivanbekunai', 'id': 'UChRz9BLuD2qEZMuvpAJ-lRQ'},
    {'name': 'nickvels_ai', 'id': 'UCgFaudM5mLnF4ixj6qeRhPQ'},
    {'name': 'igorzuevich', 'id': 'UCO85GRCGUWMH08jjBZwdq7g'},
    {'name': 'sukhov_live', 'id': 'UC4a4DzUtUjEW4tryyHoQxZQ'},
    {'name': 'yevgeniykovalenko', 'id': 'UCZefZeIiyXYIrK2KaCu41Yw'},
    {'name': 'serejaris', 'id': 'UCH6k750mdcOXU6PYHSCOlrA'},
    {'name': 'neuropros', 'id': 'UCRdFU98_6_SVmtSfhPaKDKw'},
    {'name': 'rixaihub', 'id': 'UC62WQvqor2eH87DrN3xbj_g'},
    {'name': 'rinatsuleyman', 'id': 'UCXyfe8u58vBf2aSWLQjJtVA'},
    {'name': 'aikirichenkoy', 'id': 'UCluhK-FEH0qF2s_-eHZ9B8A'}
]

# Автоматическое определение папки скрипта
base_dir = os.path.dirname(os.path.abspath(__file__))
raw_folder = os.path.join(base_dir, '00_RAW', 'YouTube')
os.makedirs(raw_folder, exist_ok=True)

def get_latest_videos_rss():
    for channel in channels:
        try:
            print(f"Парсинг YouTube (RSS): {channel['name']}")
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
                print(f"Ошибка {response.status_code} для {channel['name']}")
        except Exception as e:
            print(f"Ошибка в канале {channel['name']}: {e}")

if __name__ == '__main__':
    get_latest_videos_rss()
