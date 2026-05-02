---
source: @edvardgrishin27
date: 2026-03-20
original: https://t.me/edvardgrishin27/149
category: GOLD
tags: [Claude, AI-агент]
---

## Главная мысль
ANTHROPIC ЗАПУСТИЛА CHANNELS — CLAUDE CODE ТЕПЕРЬ РАБОТАЕТ ЧЕРЕЗ TELEGRAM И DISCORD.

## Схема / Workflow
_Не описана_

## Технические связки
- telegram → claude → anthropic
- telegram → claude

## Мясо
- ANTHROPIC ЗАПУСТИЛА CHANNELS — CLAUDE CODE ТЕПЕРЬ РАБОТАЕТ ЧЕРЕЗ TELEGRAM И DISCORD.
- Помните, я писал про Dispatch? Так вот, Anthropic не остановилась и пошла дальше — теперь Claude Code можно дёргать прямо из Telegram и Discord. Функция называется [Channels, и она в бете](https://code.claude.com/docs/en/channels).
- Суть простая: ты ставишь MCP-плагин в Claude Code, подключаешь Telegram-бота через BotFather — и всё. Пишешь боту в Телеграм задачу, Claude выполняет её в терминале на твоём компьютере и отвечает тебе в чат. Прямо как OpenClaw, только от самой Anthropic.
- Обновить Claude Code до версии 2.1.80+
- В терминале: /plugin install telegram@claude-plugins-official
- Channels — это Anthropic, которая посмотрела на то, что делает сообщество, и сказала: "Мы тоже так можем. И сделаем это нативно." И это правильный ход — большинству людей не нужна гибкость OpenClaw, им нужно чтобы работало из коробки.
