import os
import asyncio
import re
from telethon import TelegramClient
from telethon.tl.functions.search import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty, Channel

# Настройки
API_ID = 38957544
API_HASH = 'bb31ab995b5956294a2e80f619a0a3de'
SESSION_NAME = 'dan_discovery'

# Черный список (Стоп-слова для мусора)
BLACKLIST = ["крипта", "сигналы", "трейдинг", "ставки", "сигнал", "p2p", "арбитраж", "заработок", "выплаты", "инвест"]
# Белый список (Маркеры инженеров)
WHITELIST = ["интегратор", "автоматизация", "кейс", "n8n", "bitrix24", "битрикс", "amocrm", "api", "внедрение", "разработка", "схема", "workflow"]

KEYWORDS = [
    "n8n Bitrix24", "n8n amoCRM", "n8n 1C", "n8n связка", "n8n кейс",
    "Claude 3.5 API CRM", "МТС Exolve n8n", "UIS n8n",
    "ИИ-агент квалификация", "нейро-сотрудник CRM",
    "webhook CRM схема", "n8n workflow скачать"
]

async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print("🚀 Запуск Anti-Spam разведки...")
        discovered_channels = {}

        for query in KEYWORDS:
            print(f"Поиск по запросу: {query}")
            try:
                result = await client(SearchRequest(
                    q=query, 
                    limit=50, 
                    filter=InputMessagesFilterEmpty(), 
                    min_date=None, max_date=None, offset_id=0, add_offset=0, 
                    max_id=0, min_id=0, from_id=None, hash=0
                ))

                for msg in result.messages:
                    if msg.chat and isinstance(msg.chat, Channel):
                        username = msg.chat.username
                        if not username: continue
                        
                        title = (msg.chat.title or "").lower()
                        about = (msg.message or "").lower()
                        
                        if any(bad in title or bad in about for bad in BLACKLIST): continue
                        
                        if any(good in title or good in about for good in WHITELIST):
                            if username not in discovered_channels:
                                discovered_channels[username] = {
                                    'title': msg.chat.title,
                                    'text': msg.message[:200].replace('\n', ' '),
                                    'date': msg.date.strftime("%Y-%m-%d")
                                }
            except Exception as e:
                print(f"Ошибка при поиске '{query}': {e}")
            
            await asyncio.sleep(2)

        output_path = 'tg_discovered_sources.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 💎 Золотые источники Telegram (Очищено от спама)\n\n")
            for user, info in discovered_channels.items():
                f.write(f"### {info['title']}\n- **Ссылка:** https://t.me/{user}\n- **Суть:** {info['text']}\n- **Дата поста:** {info['date']}\n\n")

if __name__ == '__main__':
    asyncio.run(main())
