# GOLD: n8n / CRM / Автоматизация — дайджест (23.04.2026)

> Отфильтровано из 58 файлов 00_RAW. 12 GOLD → инбокс, 46 TRASH → #archive.

---

## 1. n8n vs ИИ-агент: архитектурный выбор
**Источник:** [zuevichigor/1959](https://t.me/zuevichigor/1959)

Ключевое различие: в n8n тратишь время на настройку **каждого нового шаблона**, ИИ-агента настраиваешь **один раз** — и он адаптируется сам. Минус: первая настройка съедает 5+ дней. Gemini CLI отработал задачу 156 раз вместо одного — пока агент не "обучился". Это нормально, это инвестиция в сотрудника.

**Инсайт для CRM:** не пиши отдельный n8n-сценарий под каждый тип лида — обучи одного агента работать с Bitrix24 через CLAUDE.md.

---

## 2. Claude Code Routines vs n8n: планировщик задач для агентов
**Источник:** [zuevichigor/1956](https://t.me/zuevichigor/1956)

- Routines напоминает n8n, но с ограничениями по расписанию
- Как обойти: настроить внешний планировщик задач (cron/systemd) + Obsidian/markdown-файлы как передача инструкций
- ТОП 50 рутинных задач для делегирования ИИ-агенту

**Видео:** https://www.youtube.com/watch?v=GBbbXlfHkS8

---

## 3. AI-сотрудник на Claude Code: HR-бот за несколько минут
**Источник:** [zuevichigor/1952](https://t.me/zuevichigor/1952)

- 5 шагов создания ИИ-помощника на базе Claude Code
- Развернуть HR-бота + подключить к Telegram — несколько минут
- На одной подписке Claude — неограниченное количество агентов через разные сессии
- Шаблоны n8n + промпты в базе: https://l.igorzuevich.com/aicl

**Видео:** https://www.youtube.com/watch?v=WADKRc4eTJw

---

## 4. Claude Code на сервере + Telegram-мост + n8n-документация
**Источник:** [zuevichigor/1957](https://t.me/zuevichigor/1957)

Практическая архитектура: Claude Code → сервер → Telegram-интерфейс (без VPN-рисков). Параллельно — Codex и Gemini CLI как резервные агенты. База из 52+ рекомендаций внедрений: скачиваешь файл, кидаешь в агент → он строит ИИ-проект с базами данных, автоматизациями, интеграциями.

**Ссылка на базу:** https://l.igorzuevich.com/aicl

---

## 5. Gemini CLI: полная настройка + Telegram-мост + трёхуровневая память
**Источник:** [zuevichigor/1958](https://t.me/zuevichigor/1958)

- Бесплатный аналог Claude Code, 2 000 000 токенов контекст
- Telegram-мост: управление агентом голосом/текстом
- Три уровня памяти: SQLite (оперативная) + Obsidian (долгосрочная) + agent.md
- Мультимодальность: фото, документы, голосовые
- Планировщик: агент просыпается и работает без участия пользователя
- 12 готовых markdown-файлов для настройки за 15 минут

**Видео:** https://www.youtube.com/watch?v=RzSbZr2orEQ

---

## 6. Codex: полный гайд — трёхуровневая память + Telegram
**Источник:** [zuevichigor/1954](https://t.me/zuevichigor/1954)

- 8 шагов настройки Codex с нуля
- Подключение к Telegram: голос, фото, видео, файлы
- Память: оперативная + долгосрочная через Obsidian + Agent.md
- 52 проверенные рекомендации для улучшения агента
- Скилы с официального GitHub OpenAI

**Видео:** https://www.youtube.com/watch?v=ozlhPa3CzQM

---

## 7. 7 команд для управления ИИ-агентом (Gemini CLI / Claude Code / Codex)
**Источник:** [zuevichigor/1960](https://t.me/zuevichigor/1960)

- Сохранение итогов сессии в долгосрочную память
- Сжатие контекстного окна для экономии токенов
- Короткие напоминания внутри сессии
- Планировщик: выполнение задач ночью без участия пользователя

**Видео:** https://www.youtube.com/watch?v=1PeBB5Nvzyw

---

## 8. Claude Managed Agents vs самосборные связки
**Источник:** [zuevichigor/1953](https://t.me/zuevichigor/1953)

Anthropic строит "ОС для агентов" — Claude Managed Agents берёт на себя управление инструментами, контекстом, памятью, цепочкой задач. Обмен: меньше головной боли → зависимость от системы. Альтернатива: свои связки с полным контролем (Claude Code + n8n + MCP).

**Инсайт:** самосборная архитектура гибче для CRM-интеграций — сегодня Bitrix24, завтра RetailCRM, без переделки с нуля.

---

## 9. Claude Managed Agents: интеграции с Notion, Rakuten, Asana
**Источник:** [edvardgrishin27/165](https://t.me/edvardgrishin27/165)

- Агенты без собственного сервера для Notion, Rakuten, Asana
- Claude Advisor Strategy: Opus думает → Sonnet делает
- Claude Code: /ultraplan (план на вебе), Monitor, /autofix-pr, iOS-виджеты
- Claude Mythos: SWE-bench 93.9% (пока не выпущен)

**Документация Managed Agents:** https://platform.claude.com/docs/en/managed-agents/overview

---

## 10. Метод Карпати: knowledge base через Obsidian без RAG
**Источник:** [edvardgrishin27/164](https://t.me/edvardgrishin27/164)

Андрей Карпати (Tesla AI, OpenAI) — метод персональной базы знаний на markdown-файлах. Без RAG, без векторных баз, без сложных пайплайнов. Применение для CRM: хранить в Obsidian промпты для ответов клиентам, шаблоны сделок, скрипты.

**Промпты и инструкции:** https://t.me/thefuturaai_bot?start=video_claudesmart
**Видео:** https://youtu.be/P7JDXCAVPxY

---

## 11. ТОП 17 плагинов для Claude Code (с GitHub-ссылками)
**Источник:** [edvardgrishin27/168](https://t.me/edvardgrishin27/168)

Реально используемые плагины с инструкциями по установке:
- **Colleague Skill** — https://github.com/titanwings/colleague-skill
- **Marketing Skills** — https://github.com/coreyhaines31/marketingskills
- **SEO Machine** — https://github.com/TheCraigHewitt/seomachine
- **AgentMemory** — https://github.com/rohitg00/agentmemory
- **RAG-Anything** — https://github.com/HKUDS/RAG-Anything
- **MemPalace** — https://github.com/MemPalace/mempalace
- **Awesome MCP Servers** — https://github.com/punkpeye/awesome-mcp-servers

**Видео:** https://youtu.be/UtEaUX8eEnM

---

## 12. Telegram Exporter: обновление (парсинг для n8n-пайплайнов)
**Источник:** [rixaihub/438](https://t.me/rixaihub/438)

Обновлённый инструмент для экспорта Telegram-каналов в markdown. Функции:
- Транскрибация голосовых через Deepgram
- Экспорт всей папки сразу → чистые .md файлы → в нейронку / n8n
- Несколько аккаунтов в одной сессии

**GitHub:** https://github.com/morf3uzzz/telegram-exporter
