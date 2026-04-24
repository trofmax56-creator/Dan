import asyncio
import os
from telethon import TelegramClient

api_id = 38957544
api_hash = 'bb31ab995b5956294a2e80f619a0a3de'
phone_number = '+79606945766'

channels = [
    'ris_ai',
    'BekinAI',
    'edvardgrishin27', 'gora_academy', 'zuevichigor', 'fomo_team', 
    'maxryzhkov', 'juliangoldieseo', 'aikirichenkoy', 'rixaihub', 
    'aiautomation_n8n', 'neuropros', 'addmeto', 'ai_newz', 
    'neural_network_news', 'denis_ai', 'adept_ecommerce'
]

raw_folder = '00_RAW'
os.makedirs(raw_folder, exist_ok=True)

# Use absolute path for session file to be sure
session_path = '/app/Dan/dan_session'
client = TelegramClient(session_path, api_id, api_hash)

async def main():
    await client.start(phone=phone_number)
    for channel in channels:
        try:
            print(f'Parsing: {channel}')
            entity = await client.get_entity(channel)
            async for message in client.iter_messages(entity, limit=10):
                if message.text and len(message.text) > 50:
                    filename = f"{raw_folder}/{channel}_{message.id}.md"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"---\ndate: {message.date}\nlink: https://t.me/{channel}/{message.id}\n---\n\n{message.text}")
        except Exception as e:
            print(f"Error in {channel}: {e}")
    print('Done!')

if __name__ == '__main__':
    client.loop.run_until_complete(main())
