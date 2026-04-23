---
title: HeyGen CLI + Claude Code — автоматические видео-КП при смене стадии сделки
tags: #biz_recipe #automation #bitrix24 #heygen #video #claude_code #action_needed
source: adept_ecommerce/403
date: 2026-04-23
---

### 1. Описание идеи

HeyGen выпустили официальный CLI, спроектированный как agent-first: все команды возвращают структурированный JSON, CLI создан для управления со стороны других агентов (Claude Code, n8n, bash-скрипты). Практическая связка для CRM: при переходе сделки в стадию «КП отправлено» → Claude Code генерирует персональный скрипт видео-приветствия → HeyGen CLI создаёт видео с аватаром менеджера → видео отправляется клиенту в WhatsApp/email. Видео-КП конвертирует на 30–40% лучше текстового.

### 2. Технический стек

- AI: Claude Sonnet 4.6 (генерация скрипта видео)
- Video: HeyGen CLI (v3 API) — https://developers.heygen.com/cli
- CRM: Bitrix24 REST API
- Middleware: n8n (триггер) + bash/Python (исполнение)
- Доставка: WhatsApp Business API / Email

### 3. Пошаговый план внедрения

**Шаг 1 — Установка HeyGen CLI**
```bash
npm install -g @heygen/cli
heygen auth login   # авторизация через API key из HeyGen dashboard
heygen avatars list --json  # получить ID своего аватара
heygen voices list --json   # получить ID голоса
```

**Шаг 2 — Триггер в Bitrix24**
```
Webhook: смена стадии сделки → "КП: видео отправить"
n8n: GET /crm.deal.get → собрать {client_name, product, manager_name, deal_id}
```

**Шаг 3 — Claude генерирует скрипт видео**
```python
import anthropic

client = anthropic.Anthropic()

VIDEO_SCRIPT_PROMPT = """
Напиши скрипт видео-сообщения для отправки клиенту. Длина: 45–60 секунд (120–150 слов).

Данные сделки:
- Клиент: {client_name}
- Продукт/услуга: {product}
- Менеджер: {manager_name}

Требования:
- Обращение по имени в первых 3 секундах
- Личный тон, не шаблонный
- Конкретная выгода для этого клиента (1 факт)
- Чёткий призыв к действию в конце
- БЕЗ слов «уникальный», «эксклюзивный», «лучший на рынке»
- Язык: разговорный русский

Верни только текст скрипта, без пояснений.
"""

def generate_video_script(deal_data: dict) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": VIDEO_SCRIPT_PROMPT.format(**deal_data)
        }]
    )
    return message.content[0].text
```

**Шаг 4 — HeyGen CLI создаёт видео**
```bash
#!/bin/bash
# generate_video.sh — принимает скрипт и возвращает URL видео

AVATAR_ID="your_avatar_id"    # из heygen avatars list
VOICE_ID="your_voice_id"      # из heygen voices list
SCRIPT="$1"
DEAL_ID="$2"

# Запуск генерации
VIDEO_JSON=$(heygen video create \
  --avatar "$AVATAR_ID" \
  --voice "$VOICE_ID" \
  --script "$SCRIPT" \
  --json)

VIDEO_ID=$(echo "$VIDEO_JSON" | jq -r '.video_id')

# Поллинг статуса (каждые 15 сек, макс 5 мин)
for i in $(seq 1 20); do
  STATUS_JSON=$(heygen video status --id "$VIDEO_ID" --json)
  STATUS=$(echo "$STATUS_JSON" | jq -r '.status')

  if [ "$STATUS" = "completed" ]; then
    VIDEO_URL=$(echo "$STATUS_JSON" | jq -r '.video_url')
    echo "$VIDEO_URL"
    exit 0
  fi

  sleep 15
done

echo "ERROR: timeout" >&2
exit 1
```

**Шаг 5 — Python-оркестратор (полный пайплайн)**
```python
import subprocess, requests, os

BITRIX_WEBHOOK = os.environ["BITRIX_WEBHOOK"]

def send_video_kp(deal_data: dict):
    # 1. Генерируем скрипт
    script = generate_video_script(deal_data)

    # 2. HeyGen CLI создаёт видео
    result = subprocess.run(
        ["bash", "generate_video.sh", script, deal_data["deal_id"]],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"HeyGen error: {result.stderr}")

    video_url = result.stdout.strip()

    # 3. Сохраняем ссылку в Bitrix24
    requests.post(f"{BITRIX_WEBHOOK}/crm.deal.update.json", json={
        "id": deal_data["deal_id"],
        "fields": {
            "COMMENTS": f"Видео-КП: {video_url}\nСкрипт: {script[:200]}..."
        }
    })

    # 4. Отправляем клиенту (через n8n WhatsApp-ноду или email)
    return video_url
```

**Шаг 6 — n8n финальная нода отправки**
```
HTTP Request → /send_video_kp (Python-сервис)
  ↓ получаем video_url
WhatsApp Business API: отправить video_url клиенту
  ↓
Bitrix24: сменить стадию → "КП: отправлено"
```

### 4. Стоимость одного видео-КП

| Компонент | Стоимость |
|-----------|-----------|
| Скрипт (Claude Sonnet, ~300 токенов) | ~$0.001 |
| HeyGen видео (60 сек, Creator план) | ~$0.15–0.25 |
| **Итого** | **~$0.15–0.25** |

При 20 видео/день = $3–5/день = ~$100/мес. Замена видеографа на аутсорсе ($200–500/видео) окупается за 1 видео.

### 5. Нюансы

- HeyGen CLI требует стабильный интернет на сервере (видео создаётся на стороне HeyGen, не локально)
- Время генерации 60-секундного видео: 2–4 минуты — не блокирует менеджера, отправляется автоматически
- Аватар нужно создать в HeyGen заранее (фото менеджера или стоковый аватар)
- Голос — можно клонировать голос менеджера в HeyGen (функция Voice Clone)
- Документация CLI: https://developers.heygen.com/cli

### 6. Оценка эффективности

- Сложность: 3/5
- ROI: видео-КП конвертируют на 30–40% лучше текстовых (данные HeyGen); персонализация по имени клиента увеличивает открываемость; автоматизация убирает 20–30 мин ручного труда на каждое видео

**Ссылки:** [[02_TOOLS/Bitrix24_API]] | [[02_TOOLS/HeyGen_CLI]] | [[03_GUIDES/n8n_whatsapp]]
