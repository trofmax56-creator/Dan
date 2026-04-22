import asyncio
import os
from telethon import TelegramClient

api_id = 38957544
api_hash = 'bb31ab995b5956294a2e80f619a0a3de'
channels = ['edvardgrishin27', 'gora_academy', 'zuevichigor']
raw_folder = '00_RAW'

os.makedirs(raw_folder, exist_ok=True)

client = TelegramClient('dan_session', api_id, api_hash)

async def main():
    await client.start()
    for channel in channels:
        try:
            print(f'Parsing: {channel}')
            entity = await client.get_entity(channel)
            async for message in client.iter_messages(entity, limit=10):
                if message.text:
                    filename = f"{raw_folder}/{channel}_{message.id}.md"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"---\ndate: {message.date}\nlink: https://t.me/{channel}/{message.id}\n---\n\n{message.text}")
        except Exception as e:
            print(f"Error in {channel}: {e}")
    print('Done! Posts saved to 00_RAW')

if __name__ == '__main__':
    client.loop.run_until_complete(main())