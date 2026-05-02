---
title: GPT Image 2 + Claude Design — автогенератор визуальных КП из данных сделки
tags: #biz_recipe #automation #bitrix24 #claude_design #gpt_image2 #marketing #action_needed
source: ai_newz/4541, edvardgrishin27/174, rixaihub/444
date: 2026-04-23
---

### 1. Описание идеи

GPT Image 2 умеет генерировать фотореалистичные изображения и чистые UI-макеты. Claude Design переводит макет в HTML/CSS. Связка: GPT Image 2 генерирует иллюстрацию продукта или обложку КП → Claude Design верстает вокруг неё полное коммерческое предложение → n8n прикрепляет PDF к сделке в Bitrix24. Результат: визуально сильное КП без дизайнера, генерируется автоматически при смене стадии.

### 2. Технический стек

- Image AI: GPT Image 2 (OpenAI API, модель `gpt-image-2`)
- Layout AI: Claude Design / Claude Opus 4.7 (верстка HTML)
- CRM: Bitrix24 REST API
- Middleware: n8n + Python (Puppeteer для HTML→PDF)
- Хранение: S3-совместимое (Hetzner Object Storage / Yandex Cloud)

### 3. Пошаговый план внедрения

**Шаг 1 — Настроить триггер в Bitrix24**
Вебхук на смену стадии сделки → `"КП: подготовить"` → передаёт в n8n: название продукта, имя клиента, цену, имя менеджера.

**Шаг 2 — Генерация иллюстрации через GPT Image 2**
```python
from openai import OpenAI
import base64, os

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_product_image(product_name: str, style: str = "photorealistic") -> bytes:
    """Генерирует обложку КП. Возвращает PNG-байты."""
    prompt = (
        f"Professional product photo for a commercial proposal. "
        f"Product: {product_name}. "
        f"Style: clean white background, {style}, high-end B2B presentation quality. "
        f"No text, no watermarks, 16:9 aspect ratio."
    )
    response = openai_client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size="1792x1024",   # поддерживает произвольные соотношения
        quality="high",
        n=1,
        response_format="b64_json"
    )
    return base64.b64decode(response.data[0].b64_json)
```

**Шаг 3 — Верстка КП через Claude Design / Claude API**
```python
import anthropic, base64

anthropic_client = anthropic.Anthropic()

KP_PROMPT = """
Ты — старший веб-дизайнер. Создай одностраничное коммерческое предложение в формате HTML.

Данные сделки:
- Клиент: {client_name}, {client_company}
- Продукт: {product}
- Стоимость: {price} руб.
- Менеджер: {manager}, {manager_phone}
- Действует до: {valid_until}

Изображение продукта приложено (используй как hero-image в верхней части).

Требования к HTML:
1. Весь CSS инлайн (стили в теге <style> внутри <head>)
2. Никаких внешних зависимостей — только system fonts (Arial, sans-serif)
3. Цветовая схема: тёмно-синий #1A2B5E + белый + акцентный золотой #C9A227
4. Секции: hero с изображением / суть предложения / выгоды (3 пункта) / цена + кнопка / контакты
5. Размер для печати A4, готов к PDF-экспорту
6. Вернуть только HTML-код, без объяснений
"""

def generate_kp_html(deal_data: dict, product_image_bytes: bytes) -> str:
    img_b64 = base64.standard_b64encode(product_image_bytes).decode("utf-8")

    message = anthropic_client.messages.create(
        model="claude-opus-4-7",
        max_tokens=8192,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": img_b64
                    }
                },
                {
                    "type": "text",
                    "text": KP_PROMPT.format(**deal_data)
                }
            ]
        }]
    )
    return message.content[0].text
```

**Шаг 4 — HTML → PDF и загрузка в Bitrix24**
```python
import subprocess, tempfile, os, requests

def html_to_pdf(html_content: str) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
        f.write(html_content)
        html_path = f.name
    pdf_path = html_path.replace(".html", ".pdf")

    subprocess.run([
        "npx", "puppeteer-cli", "print", html_path, pdf_path,
        "--format", "A4", "--margin-top", "0", "--margin-bottom", "0"
    ], check=True)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    os.unlink(html_path)
    os.unlink(pdf_path)
    return pdf_bytes


def attach_pdf_to_deal(deal_id: str, pdf_bytes: bytes, filename: str, bitrix_webhook: str):
    """Прикрепляет PDF к сделке через Bitrix24 Disk API."""
    upload_resp = requests.post(
        f"{bitrix_webhook}/disk.folder.uploadfile.json",
        data={"id": "DEAL_FOLDER_ID"},   # ID папки диска сделки
        files={"file": (filename, pdf_bytes, "application/pdf")}
    ).json()
    file_id = upload_resp["result"]["ID"]

    requests.post(f"{bitrix_webhook}/crm.deal.update.json", json={
        "id": deal_id,
        "fields": {
            "COMMENTS": f"КП сформировано автоматически. Файл ID: {file_id}"
        }
    })
    return file_id
```

**Шаг 5 — Полный пайплайн (n8n Function Node)**
```javascript
// n8n: сборка и запуск пайплайна
const dealData = {
  client_name:    $json.CONTACT_NAME,
  client_company: $json.COMPANY_TITLE,
  product:        $json.COMMENTS,
  price:          $json.OPPORTUNITY,
  manager:        $json.ASSIGNED_BY_NAME,
  manager_phone:  $json.ASSIGNED_BY_PHONE,
  valid_until:    new Date(Date.now() + 14*86400000).toLocaleDateString('ru-RU')
};

// Далее HTTP Request nodes вызывают Python-сервис последовательно:
// 1. POST /generate-image → PNG bytes
// 2. POST /generate-html  → HTML string (передаём PNG)
// 3. POST /html-to-pdf    → PDF bytes
// 4. POST /attach-to-deal → file_id в Bitrix24
return [{ json: dealData }];
```

### 4. Стоимость одного КП (оценка)

| Шаг | Модель | Стоимость |
|-----|--------|-----------|
| Генерация иллюстрации | GPT Image 2, high quality | ~$0.04–0.08 |
| Верстка HTML | Claude Opus 4.7, ~3000 токенов | ~$0.07 |
| PDF конвертация | Puppeteer (свой сервер) | ~$0.00 |
| **Итого** | | **~$0.12–0.15 за КП** |

При 20 КП в день = ~$3/день = ~$90/мес. Экономия на дизайнере (4–8 ч/день) существенно перекрывает.

### 5. Ограничения

- GPT Image 2: фирменные цвета и логотип в иллюстрации — только через inpainting или img2img (пока недоступно в базовом API). Лого вставлять программно через Pillow поверх сгенерированного изображения
- Claude Opus 4.7: новый токенизатор — длинный промпт + изображение может стоить на 20–35% дороже, чем ожидаете по старым расчётам
- Сервер: для HTML→PDF через Puppeteer нужен Node.js. На Hetzner CX21 (€3.79/мес) достаточно

### 6. Оценка эффективности

- Сложность: 4/5
- ROI: КП без дизайнера за 45–90 секунд vs 2–4 часа с дизайнером; при потоке 20+ сделок/день = полноценная замена дизайнера на аутсорсе ($500–1000/мес); конверсия в ответ клиента растёт за счёт скорости отправки (пока горячий интерес)

**Ссылки:** [[02_TOOLS/Bitrix24_API]] | [[02_TOOLS/OpenAI_ImageAPI]] | [[claude.ai/design]]
