import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import SearchGlobalRequest
from telethon.tl.types import InputMessagesFilterEmpty, InputPeerEmpty, Channel

# Настройки (из профиля Максима)
API_ID = 38957544
API_HASH = 'bb31ab995b5956294a2e80f619a0a3de'
# Используем существующую авторизованную сессию из корня проекта
SESSION_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dan_session')

# Черный список (Стоп-слова для мусора)
BLACKLIST = [
    "крипта", "сигналы", "трейдинг", "ставки", "сигнал", "p2p", "арбитраж",
    "заработок", "выплаты", "казино", "инвестиции крипта", "сигналы трейдинг",
    "украин", "повестк", "онлайн-профессии", "девочки", "заработок онлайн",
    "форекс", "нфт", "nft", "майнинг",
]
# Белый список — язык AI/n8n практиков (как пишут целевые каналы)
WHITELIST = [
    "n8n", "make.com", "zapier", "автоматизация",
    "gpt", "claude", "chatgpt", "gemini", "llm", "нейросеть",
    "агент", "ai agent", "промпт", "prompt",
    "workflow", "api", "python", "telegram бот",
    "obsidian", "notion", "второй мозг",
    "midjourney", "stable diffusion", "генерация",
]

# Короткие запросы — больше результатов от Telegram Search
KEYWORDS = [
    "n8n автоматизация",
    "chatgpt кейс",
    "AI агент",
    "нейросеть бизнес",
    "prompt engineering",
    "llm агент",
    "make.com автоматизация",
    "claude api",
    "второй мозг",
    "нейросети инструменты",
    "gpt автоматизация",
    "telegram бот gpt",
    "obsidian notion",
    "ии рутина",
    "автоматизация workflow",
]

async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print("🚀 Запуск Discovery v2 (Engineer Focus)...")
        discovered_channels = {}

        for query in KEYWORDS:
            print(f"Поиск по зацепке: {query}")
            try:
                result = await client(SearchGlobalRequest(
                    q=query,
                    filter=InputMessagesFilterEmpty(),
                    min_date=None,
                    max_date=None,
                    offset_rate=0,
                    offset_peer=InputPeerEmpty(),
                    offset_id=0,
                    limit=100
                ))

                chats_by_id = {c.id: c for c in getattr(result, 'chats', [])}

                for msg in result.messages:
                    peer_id = getattr(getattr(msg, 'peer_id', None), 'channel_id', None)
                    chat = chats_by_id.get(peer_id)
                    
                    if chat and isinstance(chat, Channel) and chat.username:
                        username = chat.username
                        title = (chat.title or "").lower()
                        text = (msg.message or "").lower()
                        
                        if any(bad in title or bad in text for bad in BLACKLIST):
                            continue

                        views = getattr(msg, 'views', 0) or 0
                        if views > 20:
                            if username not in discovered_channels:
                                discovered_channels[username] = {
                                    'title': chat.title,
                                    'text': (msg.message or '')[:250].replace('\n', ' '),
                                    'date': msg.date.strftime("%Y-%m-%d"),
                                    'views': views
                                }
            except Exception as e:
                print(f"Ошибка поиска '{query}': {e}")

            await asyncio.sleep(2)

        output_path = os.path.join(os.path.dirname(__file__), 'tg_discovered_v2.md')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 💎 Золотые источники Telegram v2 (Математический отбор)\n\n")
            f.write("Найдены каналы с высоким ERR и техническим контентом (LLM, RAG, Workflow).\n\n")
            sorted_channels = sorted(discovered_channels.items(), key=lambda x: x[1]['views'], reverse=True)
            
            for user, info in sorted_channels:
                f.write(f"### {info['title']} (Просмотров поста: {info['views']})\n")
                f.write(f"- **Ссылка:** https://t.me/{user}\n")
                f.write(f"- **Тех. контекст:** {info['text']}\n")
                f.write(f"- **Дата:** {info['date']}\n\n")
        
        print(f"✅ Найдено качественных каналов: {len(discovered_channels)}")

if __name__ == '__main__':
    asyncio.run(main())
