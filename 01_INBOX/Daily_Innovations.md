# Daily Innovations — 2026-04-24
*Скан 00_RAW за 24ч | Найдено 3 GOLD-кейса автоматизации*

---

## Кейс 1: HeyGen CLI — agent-first видео-КП без HTTP-костылей

**Источник:** [adept_ecommerce/403](https://t.me/adept_ecommerce/403) | 2026-04-13  
**Рецепт:** `05_BIZ_RECIPES/064_heygen_cli_video_kp_crm.md`

### 1. В чём инновация
HeyGen выпустили официальный CLI, изначально спроектированный как **agent-first**: все команды возвращают структурированный JSON. Раньше для интеграции нужно было вручную собирать HTTP-запросы, ловить статусы и парсить ответы. Теперь одна строка bash:
```bash
heygen video create --avatar manager_id --script "Привет, Иван..." | jq '.video_id'
```
Claude Code или n8n управляют созданием видео напрямую, без «костылей» с вебхуками.

### 2. Как внедрить нам
1. Установить: `npm install -g @heygen/cli` + `heygen auth login`
2. В Bitrix24 настроить webhook при переходе сделки в стадию «КП отправлено»
3. n8n принимает webhook → HTTP Request к Claude API (Sonnet 4.6) → генерирует персональный скрипт видео из данных сделки
4. n8n → Execute Command: `heygen video create --avatar {manager_id} --script "..."` → polling `heygen video status {id}` каждые 30 сек
5. После готовности: `heygen video download {id}` → отправить в WhatsApp/email клиенту + прикрепить к сделке
6. Конверсия видео-КП выше текстового на 30–40% — результат измеряем через UTM в ссылке внутри видео

### 3. Связи с рецептами
- **064** `064_heygen_cli_video_kp_crm.md` — основной рецепт, подтверждён релизом CLI
- **058** `058_claude_code_vps_telegram_crm_agent.md` — инфраструктура VPS+Telegram для запуска CLI

---

## Кейс 2: Claude Code cron + Obsidian — обход лимитов Routines для ночного агента

**Источник:** [zuevichigor/1956](https://t.me/zuevichigor/1956) | 2026-04-16  
**Рецепт:** `05_BIZ_RECIPES/060_claude_code_routines_cron_bitrix_moysklad.md`

### 1. В чём инновация
Claude Code Routines ограничены по частоте и не поддерживают сложные многоступенчатые инструкции. Зуевич показывает обходной путь: **cron на VPS запускает `claude --print` с инструкцией из markdown-файла**. Любой `.md`-документ в Obsidian превращается в «задание» для агента. Это работает не только с Claude Code — та же схема применима к Codex и Gemini CLI.

Ключевая идея: **инструкции живут в версионируемых markdown-файлах**, а не в интерфейсе Routines. Можно менять поведение агента без трогания cron — просто обновляешь файл.

### 2. Как внедрить нам
1. На VPS создать папку `~/routines/` с файлами инструкций:
   - `morning_crm.md` — проверить просроченные задачи Bitrix24, сформировать отчёт
   - `stock_check.md` — сверить остатки в МойСклад, уведомить о критических
   - `overdue_deals.md` — найти сделки без активности 3+ дней, написать напоминание
2. Crontab:
   ```
   0 8  * * 1-5  claude --print -p "$(cat ~/routines/morning_crm.md)" | telegram-send -
   0 22 * * 1-5  claude --print -p "$(cat ~/routines/stock_check.md)"
   ```
3. Результаты агента → bash-скрипт → Telegram Bot API → утренний дайджест менеджеру
4. Markdown-файлы инструкций синхронизировать через Obsidian + Git для версионирования

### 3. Связи с рецептами
- **060** `060_claude_code_routines_cron_bitrix_moysklad.md` — полный рецепт с bash-обёрткой и кодом
- **058** `058_claude_code_vps_telegram_crm_agent.md` — VPS-инфраструктура + Telegram-доставка

---

## Кейс 3: GPT Image 2 → Claude Design → PDF КП — конвейер визуальных предложений без дизайнера

**Источники:** [ai_newz/4541](https://t.me/ai_newz/4541), [rixaihub/444](https://t.me/rixaihub/444), [edvardgrishin27/170](https://t.me/edvardgrishin27/170) | 2026-04-21–22  
**Рецепты:** `05_BIZ_RECIPES/063_gpt_image2_claude_design_kp_generator.md`, `05_BIZ_RECIPES/061_claude_design_crm_brand_kit.md`

### 1. В чём инновация
Два события совпали: GPT Image 2 (релиз 21.04) и Claude Design (релиз 17.04) создают **полный pipeline без дизайнера**:

- **GPT Image 2** — первая «думающая» модель генерации изображений: сама гуглит инфу, строит композицию, выдаёт до 8 консистентных изображений за промпт. Рендерит чистые UI-макеты и обложки продуктов на уровне профессионала.
- **Claude Design** — принимает изображение или описание, верстает вокруг него полноценное КП с брендбуком компании. Экспорт HTML/PDF/PPTX. Один кейс из rixaihub: 14 часов ручной работы → 15 минут с Claude Design.

Комбинация: GPT Image 2 генерирует иллюстрацию → Claude Design собирает КП → PDF прикрепляется к сделке.

### 2. Как внедрить нам
1. Bitrix24 webhook при переходе сделки в стадию «Подготовка КП»
2. n8n → Claude Sonnet 4.6: извлечь описание продукта/услуги из карточки сделки
3. n8n → OpenAI API `gpt-image-2` (2K resolution): сгенерировать обложку КП/иллюстрацию продукта
4. n8n → Claude Opus 4.7 (claude.ai/design или API): передать изображение + данные клиента → сгенерировать HTML-КП в фирменном стиле
5. Puppeteer: HTML → PDF (headless Chrome на VPS)
6. Bitrix24 REST API: прикрепить PDF к сделке + отправить клиенту через email/WhatsApp

**Экономия:** дизайнер КП — 2–4 часа → агент — 3–5 минут. ROI считается с первого же использования.

### 3. Связи с рецептами
- **063** `063_gpt_image2_claude_design_kp_generator.md` — полный рецепт с n8n-схемой
- **061** `061_claude_design_crm_brand_kit.md` — настройка памяти бренда в Claude Design
- **062** `062_opus47_pdf_contracts_to_crm.md` — смежный рецепт: Opus 4.7 + PDF для контрактов

---

*Сгенерировано: 2026-04-24 | Источник: 00_RAW | Фильтр: GOLD*
