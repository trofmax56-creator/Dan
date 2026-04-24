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

raw_folder = '00_RAW/YouTube'

def get_latest_videos():
    for channel in channels:
        try:
            print(f"Парсинг YouTube канала: {channel}")
            # Получаем последние 2 видео для экономии
            cmd = [
                'yt-dlp', 
                '--get-title', '--get-id', '--get-description',
                '--playlist-items', '1-2',
                channel
            ]
            result = subprocess.check_output(cmd).decode('utf-8').split('\n')
            
            # Сохраняем в файл
            if len(result) >= 2:
                title = result[0]
                video_id = result[1]
                filename = f"{raw_folder}/{video_id}.md"
                if not os.path.exists('00_RAW/YouTube'):
                    os.makedirs('00_RAW/YouTube', exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"---\ntitle: {title}\nlink: https://youtube.com/watch?v={video_id}\n---\n\n{title}")
        except Exception as e:
            print(f"Ошибка в канале {channel}: {e}")

if __name__ == '__main__':
    get_latest_videos()
