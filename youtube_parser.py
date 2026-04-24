import os
import json
import subprocess

channels = [
    'https://youtube.com/@ivanbekunai',
    'https://youtube.com/@nickvels_ai',
    'https://youtube.com/@igorzuevich',
    'https://youtube.com/@sukhov_live',
    'https://youtube.com/@yevgeniykovalenko',
    'https://youtube.com/@serejaris',
    'https://youtube.com/@neuropros',
    'https://youtube.com/@rixaihub',
    'https://youtube.com/@rinatsuleyman',
    'https://youtube.com/@aikirichenkoy'
]

# Автоматическое определение папки
base_dir = os.path.dirname(os.path.abspath(__file__))
raw_folder = os.path.join(base_dir, '00_RAW', 'YouTube')
os.makedirs(raw_folder, exist_ok=True)

def get_latest_videos():
    for channel in channels:
        try:
            print(f"Парсинг YouTube канала: {channel}")
            # Вызываем yt-dlp через модуль python для стабильности
            cmd = [
                'python3', '-m', 'yt_dlp', 
                '--get-title', '--get-id', 
                '--playlist-items', '1-2',
                channel
            ]
            result = subprocess.check_output(cmd).decode('utf-8').split('\n')
            
            if len(result) >= 2:
                title = result[0]
                video_id = result[1]
                filename = f"{video_id}.md"
                full_path = os.path.join(raw_folder, filename)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(f"---\ntitle: {title}\nlink: https://youtube.com/watch?v={video_id}\n---\n\n{title}")
        except Exception as e:
            print(f"Ошибка в канале {channel}: {e}")

if __name__ == '__main__':
    get_latest_videos()
