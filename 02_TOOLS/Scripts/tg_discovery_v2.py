import os
import asyncio
import re
from telethon import TelegramClient
from telethon.tl.types import Channel

API_ID = 38957544
API_HASH = 'bb31ab995b5956294a2e80f619a0a3de'
SESSION_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dan_session')

# Стартовые каналы — известные AI/n8n практики
SEED_CHANNELS = [
    'edvardgrishin27', 'gora_academy', 'zuevichigor', 'FomoTeam0x',
    'maxryzhkov', 'romarayt', 'aikirichenko', 'rixaihub',
    'addmeto', 'ai_newz', 'neural_network_news', 'denis_ai',
    'adept_ecommerce', 'alexyarygin'
]

BLACKLIST = [
    "крипта", "сигналы", "трейдинг", "ставки", "сигнал", "p2p", "арбитраж",
    "заработок", "выплаты", "казино", "форекс", "нфт", "nft", "майнинг",
    "нейрографика", "подсознани", "ретрит", "эзотерик",
    "саморазвити", "трансформаци", "подработк", "тревожн",
    "похуд", "диет", "астролог", "гадан",
]

MESSAGES_PER_CHANNEL = 50

async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print("🚀 Запуск Discovery v2 (Graph Walk Mode)...")
        print(f"Сканирую {len(SEED_CHANNELS)} стартовых каналов, {MESSAGES_PER_CHANNEL} постов каждый\n")

        seed_usernames = {s.lower() for s in SEED_CHANNELS}
        discovered = {}

        for seed in SEED_CHANNELS:
            print(f"📡 Сканирую: @{seed}")
            try:
                entity = await client.get_entity(seed)
                count = 0
                async for msg in client.iter_messages(entity, limit=MESSAGES_PER_CHANNEL):
                    if not msg.message:
                        continue
                    links = re.findall(r't\.me/([a-zA-Z0-9_]+)', msg.message)
                    for username in links:
                        uname_lower = username.lower()
                        if uname_lower in seed_usernames:
                            continue
                        if uname_lower in discovered:
                            discovered[uname_lower]['mentions'] += 1
                            discovered[uname_lower]['sources'].add(seed)
                            continue
                        try:
                            ch = await client.get_entity(username)
                            if not isinstance(ch, Channel) or not ch.username:
                                continue
                            title = ch.title or ''
                            title_lower = title.lower()
                            if any(bad in title_lower for bad in BLACKLIST):
                                continue
                            views = 0
                            async for last_msg in client.iter_messages(ch, limit=1):
                                views = getattr(last_msg, 'views', 0) or 0
                            discovered[uname_lower] = {
                                'username': ch.username,
                                'title': title,
                                'mentions': 1,
                                'views': views,
                                'sources': {seed},
                            }
                            count += 1
                            print(f"  ✅ @{ch.username} — {title} (👁 {views})")
                        except Exception:
                            pass
                        await asyncio.sleep(0.3)
                print(f"  → Новых каналов найдено: {count}")
            except Exception as e:
                print(f"  ⚠️ Ошибка @{seed}: {e}")
            await asyncio.sleep(1)

        sorted_channels = sorted(
            discovered.values(),
            key=lambda x: (x['mentions'], x['views']),
            reverse=True
        )

        output_path = os.path.join(os.path.dirname(__file__), 'tg_discovered_v2.md')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 💎 Золотые источники Telegram v2 (Graph Walk)\n\n")
            f.write(f"Каналы, которые рекомендуют AI-практики: **{len(sorted_channels)}**\n\n")
            for ch in sorted_channels:
                sources = ', '.join(f'@{s}' for s in ch['sources'])
                f.write(f"### {ch['title']}\n")
                f.write(f"- **Ссылка:** https://t.me/{ch['username']}\n")
                f.write(f"- **Упоминаний:** {ch['mentions']}\n")
                f.write(f"- **Просмотров последнего поста:** {ch['views']}\n")
                f.write(f"- **Кто рекомендует:** {sources}\n\n")

        print(f"\n✅ Итого найдено: {len(sorted_channels)} каналов")
        print(f"📄 Результат: {output_path}")

if __name__ == '__main__':
    asyncio.run(main())
