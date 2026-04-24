# Daily Ideas — 2026-04-24
*Скан 00_RAW за 24ч | Все GOLD-находки по автоматизации*

---

## GOLD — Кейсы автоматизации

### 1. HeyGen CLI — agent-first видео
Официальный CLI HeyGen v3 API. Все команды → JSON. Claude Code или n8n управляют видеогенерацией из терминала без HTTP-костылей. Pipeline: CRM триггер → скрипт → видео → WhatsApp клиенту.  
→ [adept_ecommerce/403](https://t.me/adept_ecommerce/403) | Рецепт: `064`

### 2. Cron + Obsidian → обход лимитов Claude Routines
`claude --print -p "$(cat task.md)"` через cron. Markdown-файл = инструкция агенту. Меняешь файл — меняешь поведение агента без перенастройки расписания. Работает с Claude Code, Codex, Gemini.  
→ [zuevichigor/1956](https://t.me/zuevichigor/1956) | Рецепт: `060`

### 3. GPT Image 2 + Claude Design → PDF КП
GPT Image 2 генерирует UI-макеты/обложки (thinking, до 8 изображений). Claude Design верстает КП в брендбуке. Puppeteer → PDF → CRM. 14 часов ручной работы → 15 минут.  
→ [ai_newz/4541](https://t.me/ai_newz/4541), [rixaihub/444](https://t.me/rixaihub/444) | Рецепты: `063`, `061`

### 4. Claude Design — память бренда
Загружаешь логотип/сайт один раз → все последующие КП, лендинги, презентации автоматически в фирменном стиле. Без дизайнера. Экспорт: HTML, PDF, PPTX, Canva.  
→ [rixaihub/444](https://t.me/rixaihub/444), [edvardgrishin27/170](https://t.me/edvardgrishin27/170) | Рецепт: `061`

### 5. Chromium-плагин для Claude/Gemini без VPN
Open-source расширение (GitHub: Aimagine-life/gemini-unblock). Точечный прокси только для нужных сервисов — остальной интернет работает напрямую. Добавление любых сайтов через UI. Актуально для команды в РФ.  
→ [adept_ecommerce/402](https://t.me/adept_ecommerce/402), [adept_ecommerce/404](https://t.me/adept_ecommerce/404)

### 6. Claude Code Desktop — мультисессии
Полный редизайн: сайдбар с активными сессиями, встроенный терминал + diff viewer, drag-and-drop панели, Side Chat (⌘+;). Три режима: Verbose / Normal / Summary. SSH на Mac.  
→ [edvardgrishin27/167](https://t.me/edvardgrishin27/167)

### 7. Claude /dream — консолидация памяти агента
Новая команда `/dream` в Claude Code: консолидирует, исправляет и оптимизирует память агента между сессиями. Агент становится умнее с каждым использованием — помнит контекст проекта и клиентов.  
→ [BekinAI/41](https://t.me/BekinAI/41)

### 8. Kimi K2.6 — 300 параллельных субагентов
Moonshot обновили Kimi K2.6: модель обучена использовать до 300 субагентов параллельно. Применимо для масштабного сбора данных, мониторинга цен конкурентов, массовой обработки документов.  
→ [ai_newz/4539](https://t.me/ai_newz/4539)

---

## TRASH — Пропущено
- Новости о конкурентах без практического гайда (GPT 5.5, Qwen 3.6 веса)
- Мотивационные посты (gora_academy/1345)
- Реклама фокус-групп и курсов (rixaihub/446, 452)
- Вопросы про монтажёров, геймдев (adept_ecommerce/407, BekinAI/35, 37)

---

*Сгенерировано: 2026-04-24 | 157 файлов просканировано | GOLD: 8 идей | TRASH: 4 категории*
