import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.search import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty

# Настройки (из профиля Максима)
API_ID = 38957544
API_HASH = 'bb31ab995b5956294a2e80f619a0a3de'
SESSION_NAME = 'dan_discovery'

# Матрица поисковых связок
KEYWORDS = [
    "n8n Bitrix24", "n8n amoCRM", "n8n 1C", "n8n связка", "n8n кейс",
    "Claude 3.5 API CRM", "Claude 3.5 промпт", "Claude 3.5 автоматизация",
    "МТС Exolve n8n", "UIS n8n", "телефония ИИ", "автоматизация звонков",
    "ИИ-агент квалификация", "ИИ-агент продажи", "нейро-сотрудник CRM",
    "webhook CRM схема", "n8n workflow скачать", "автоматизация маркетинга n8n"
]

async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print("Запуск разведки Telegram...")
        discovered_channels = {}

        for query in KEYWORDS:
            print(f"Поиск по запросу: {query}")
            try:
                result = await client(SearchRequest(
                    q=query,
                    limit=20,
                    filter=InputMessagesFilterEmpty(),
                    min_date=None,
                    max_date=None,
                    offset_id=0,
                    add_offset=0,
                    max_id=0,
                    min_id=0,
                    from_id=None,
                    hash=0
                ))

                for msg in result.messages:
                    if msg.chat and hasattr(msg.chat, 'username') and msg.chat.username:
                        username = msg.chat.username
                        if username not in discovered_channels:
                            discovered_channels[username] = {
                                'title': getattr(msg.chat, 'title', username),
                                'last_msg': msg.message[:200].replace('\n', ' '),
                                'date': msg.date.strftime("%Y-%m-%d")
                            }
            except Exception as e:
                print(f"Ошибка при поиске '{query}': {e}")
            
            await asyncio.sleep(1)

        output_path = 'tg_discovered_sources.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 🕵️ Результаты разведки Telegram\n\n")
            f.write("| Канал | Описание/Пост | Дата поста |\n")
            f.write("| :--- | :--- | :--- |\n")
            for username, info in discovered_channels.items():
                f.write(f"| [@{username}](https://t.me/{username}) | {info['last_msg']} | {info['date']} |\n")
        
        print(f"Разведка окончена. Найдено каналов: {len(discovered_channels)}")

if __name__ == '__main__':
    asyncio.run(main())
