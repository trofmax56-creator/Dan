import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import SearchGlobalRequest
from telethon.tl.types import InputMessagesFilterEmpty, InputPeerEmpty

# Настройки
API_ID = 38957544
API_HASH = 'bb31ab995b5956294a2e80f619a0a3de'
PHONE = '+79606945766'
# Используем существующую авторизованную сессию из корня проекта
SESSION_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dan_session')

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
                result = await client(SearchGlobalRequest(
                    q=query,
                    filter=InputMessagesFilterEmpty(),
                    min_date=None,
                    max_date=None,
                    offset_rate=0,
                    offset_peer=InputPeerEmpty(),
                    offset_id=0,
                    limit=20
                ))

                # Строим словарь chat_id -> chat из result.chats
                chats_by_id = {c.id: c for c in getattr(result, 'chats', [])}

                for msg in result.messages:
                    peer_id = getattr(getattr(msg, 'peer_id', None), 'channel_id', None)
                    chat = chats_by_id.get(peer_id)
                    if chat and hasattr(chat, 'username') and chat.username:
                        username = chat.username

                        title = (getattr(chat, 'title', '') or "").lower()
                        about = (msg.message or "").lower()

                        if any(bad in title or bad in about for bad in BLACKLIST):
                            continue

                        if any(good in title or good in about for good in WHITELIST):
                            if username not in discovered_channels:
                                discovered_channels[username] = {
                                    'title': getattr(chat, 'title', username),
                                    'text': (msg.message or '')[:200].replace('\n', ' '),
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
