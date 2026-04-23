import asyncio
import os
import subprocess
from datetime import datetime
from telethon import TelegramClient

api_id = 38957544
api_hash = 'bb31ab995b5956294a2e80f619a0a3de'
phone_number = '+79606945766'

channels = [
    'edvardgrishin27', 'gora_academy', 'zuevichigor', 'fomo_team', 
    'maxryzhkov', 'juliangoldieseo', 'aikirichenkoy', 'rixaihub', 
    'aiautomation_n8n', 'neuropros', 'addmeto', 'ai_newz', 
    'neural_network_news', 'denis_ai', 'adept_ecommerce'
]

# Организация папок по датам
today = datetime.now().strftime('%Y-%m-%d')
raw_root = '00_RAW'
daily_folder = os.path.join(raw_root, today)
os.makedirs(daily_folder, exist_ok=True)

def run_git(commands):
    for cmd in commands:
        subprocess.run(cmd, shell=True)

async def main():
    # 1. Синхронизация с GitHub
    print("Обновляем локальные файлы...")
    run_git(['git pull'])

    # 2. Парсим Telegram
    client = TelegramClient('dan_session', api_id, api_hash)
    await client.start(phone=phone_number)
    
    print(f"Начинаем парсинг в папку: {daily_folder}")
    
    for channel in channels:
        try:
            print(f'Parsing: {channel}')
            entity = await client.get_entity(channel)
            async for message in client.iter_messages(entity, limit=10):
                if message.text and len(message.text) > 50:
                    filename = f"{daily_folder}/{channel}_{message.id}.md"
                    if not os.path.exists(filename):
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(f"---\ndate: {message.date}\nlink: https://t.me/{channel}/{message.id}\n---\n\n{message.text}")
        except Exception as e:
            print(f"Error in {channel}: {e}")
    
    await client.disconnect()

    # 3. Авто-пуш в GitHub
    print("Отправляем новые данные...")
    run_git([
        'git add .',
        'git commit -m "Daily auto-sync: ' + today + '"',
        'git push origin main'
    ])
    print(f"Done! Все посты за {today} в облаке.")

if __name__ == '__main__':
    asyncio.run(main())