import asyncio
import os
from telethon import TelegramClient

# Данные пользователя
api_id = 38957544
api_hash = 'bb31ab995b5956294a2e80f619a0a3de'
channels = ['edvardgrishin27', 'gora_academy', 'zuevichigor']
raw_folder = '00_RAW'

os.makedirs(raw_folder, exist_ok=True)

client = TelegramClient('dan_session', api_id, api_hash)

async def main():
    await client.start()
    for channel in channels:
        print(f'Парсим канал: {channel}')
        entity = await client.get_entity(channel)
        async for message in client.iter_messages(entity, limit=5):
            if message.text:
                filename = f"{raw_folder}/{channel}_{message.id}.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"--- \ndate: {message.date} \nlink: https://t.me/{channel}/{message.id} \n--- \n\n{message.text}")
    print('Готово! Все последние посты в 00_RAW')

with client:
    client.loop.run_until_complete(main())