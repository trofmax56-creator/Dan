import asyncio
import os
from telethon import TelegramClient

api_id = 38957544
api_hash = 'bb31ab995b5956294a2e80f619a0a3de'
phone_number = '+79606945766'

channels = [
    'ris_ai',
    'BekinAI',
    'edvardgrishin27', 'gora_academy', 'zuevichigor', 'FomoTeam0x',
    'maxryzhkov', 'romarayt', 'aikirichenko', 'rixaihub',
    'addmeto', 'ai_newz',
    'neural_network_news', 'denis_ai', 'adept_ecommerce',
    'alexyarygin'
]

# Автоматическое определение папки скрипта
base_dir = os.path.dirname(os.path.abspath(__file__))
raw_folder = os.path.join(base_dir, '00_RAW', 'Telegram')
os.makedirs(raw_folder, exist_ok=True)

session_path = os.path.join(base_dir, 'dan_session')
client = TelegramClient(session_path, api_id, api_hash)

async def main():
    await client.start(phone=phone_number)
    for channel in channels:
        try:
            print(f'Парсинг: {channel}')
            entity = await client.get_entity(channel)
            async for message in client.iter_messages(entity, limit=10):
                if message.text and len(message.text) > 50:
                    filename = f"{channel}_{message.id}.md"
                    full_path = os.path.join(raw_folder, filename)
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(f"---\ndate: {message.date}\nlink: https://t.me/{channel}/{message.id}\n---\n\n{message.text}")
        except Exception as e:
            print(f"Ошибка в {channel}: {e}")
    print('Готово!')

if __name__ == '__main__':
    client.loop.run_until_complete(main())
