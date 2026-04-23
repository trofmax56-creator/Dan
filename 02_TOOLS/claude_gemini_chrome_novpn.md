---
title: Chrome-плагин для работы с Claude/Gemini без VPN (Россия)
tags: #tool #claude #gemini #novpn #chrome #opensource
source: adept_ecommerce/402, adept_ecommerce/404
date: 2026-04-23
---

## Проблема

Claude и Gemini ограничены для российских IP. VPN тормозит весь интернет и периодически отваливается.

## Решение

Open-source расширение для Chromium — точечно пускает трафик к AI-сервисам через прокси. Весь остальной интернет работает напрямую, без VPN.

**GitHub:** https://github.com/Aimagine-life/gemini-unblock

## Поддерживаемые сервисы (по умолчанию)

- Claude (claude.ai, anthropic.com)
- Gemini (gemini.google.com)
- ElevenLabs

Можно добавить любой другой сайт через настройки.

## Установка

1. Скачать ZIP с GitHub
2. Chrome → `chrome://extensions/` → Режим разработчика → Загрузить распакованное расширение
3. В настройках плагина: добавить прокси в формате `IP:Port` или `login:password@IP:Port`
4. Видеоинструкция (7 мин): https://youtu.be/F4v2LGxWsbI

## Нюансы

- Плагин проверяет блэк-листы РКН и не проксирует запрещённые сайты
- Работает только с сайтами с гео-ограничениями, не с заблокированными РКН
- Для команды: каждый сотрудник ставит плагин на свой Chrome, один общий прокси-сервер
- Рекомендуемый прокси: Hetzner VPS (Германия) с Squid — ~€3.79/мес, хватает на 5–10 человек
