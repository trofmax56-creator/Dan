import os
import asyncio
import re
from telethon import TelegramClient
from telethon.tl.types import Channel

API_ID = 38957544
API_HASH = 'bb31ab995b5956294a2e80f619a0a3de'
SESSION_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dan_session')

# Уже известные каналы — исключаем из результатов
KNOWN_CHANNELS = {
    'ris_ai', 'bekinai', 'edvardgrishin27', 'gora_academy', 'zuevichigor',
    'fomoteam0x', 'maxryzhkov', 'romarayt', 'aikirichenko', 'rixaihub',
    'addmeto', 'ai_newz', 'neural_network_news', 'denis_ai',
    'adept_ecommerce', 'alexyarygin',
}

BLACKLIST = [
    "крипта", "крипто", "сигналы", "трейдинг", "ставки", "сигнал", "p2p",
    "арбитраж", "заработок", "заработай", "выплаты", "казино", "форекс",
    "нфт", "nft", "майнинг", "shitcoin",
    "нейрографика", "подсознани", "ретрит", "эзотерик",
    "саморазвити", "трансформаци", "подработк", "тревожн",
    "похуд", "диет", "астролог", "гадан",
    "стоик", "стоицизм", "ozon", " wb ", "маркетплейс", "wildberries",
]

RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../00_RAW/Telegram')


def extract_links_from_raw():
    """Читает все .md файлы от parser.py и считает упоминания t.me/ ссылок."""
    mentions = {}
    sources = {}

    for fname in os.listdir(RAW_DIR):
        if not fname.endswith('.md'):
            continue
        # Имя файла: channelname_msgid.md
        seed = fname.rsplit('_', 1)[0].lower()
        fpath = os.path.join(RAW_DIR, fname)
        with open(fpath, encoding='utf-8') as f:
            text = f.read()

        links = re.findall(r't\.me/([a-zA-Z0-9_]+)', text)
        for username in links:
            uname_lower = username.lower()
            # Пропускаем боты, известные каналы и технические ссылки
            if uname_lower.endswith('_bot') or uname_lower in KNOWN_CHANNELS:
                continue
            if len(uname_lower) < 3:
                continue
            mentions[uname_lower] = mentions.get(uname_lower, 0) + 1
            sources.setdefault(uname_lower, set()).add(seed)

    return mentions, sources


async def main():
    print("🚀 Discovery v2 (Graph Walk — читаю файлы от parser.py)...")
    print(f"📂 Папка: {RAW_DIR}\n")

    mentions, sources = extract_links_from_raw()
    print(f"Найдено уникальных ссылок для проверки: {len(mentions)}\n")

    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        discovered = []

        for username, count in sorted(mentions.items(), key=lambda x: -x[1]):
            try:
                entity = await client.get_entity(username)
                if not isinstance(entity, Channel):
                    continue

                title = entity.title or ''
                title_lower = title.lower()

                if any(bad in title_lower for bad in BLACKLIST):
                    print(f"  🚫 @{username} — {title} (blacklist)")
                    continue

                views = 0
                async for msg in client.iter_messages(entity, limit=1):
                    views = getattr(msg, 'views', 0) or 0

                discovered.append({
                    'username': entity.username or username,
                    'title': title,
                    'mentions': count,
                    'views': views,
                    'sources': sources[username],
                })
                print(f"  ✅ @{username} — {title} | упом: {count} | 👁 {views}")
            except Exception as e:
                print(f"  ⚠️ @{username}: {e}")
            await asyncio.sleep(0.5)

    # Сортируем: сначала по упоминаниям, потом по просмотрам
    discovered.sort(key=lambda x: (x['mentions'], x['views']), reverse=True)

    output_path = os.path.join(os.path.dirname(__file__), 'tg_discovered_v2.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 💎 Золотые источники Telegram v2 (Graph Walk)\n\n")
        f.write(f"Каналы из экосистемы AI-практиков: **{len(discovered)}**\n\n")
        for ch in discovered:
            src = ', '.join(f'@{s}' for s in sorted(ch['sources']))
            f.write(f"### {ch['title']}\n")
            f.write(f"- **Ссылка:** https://t.me/{ch['username']}\n")
            f.write(f"- **Упоминаний:** {ch['mentions']}\n")
            f.write(f"- **Просмотров последнего поста:** {ch['views']}\n")
            f.write(f"- **Кто рекомендует:** {src}\n\n")

    print(f"\n✅ Итого: {len(discovered)} каналов")
    print(f"📄 Сохранено: {output_path}")


if __name__ == '__main__':
    asyncio.run(main())
