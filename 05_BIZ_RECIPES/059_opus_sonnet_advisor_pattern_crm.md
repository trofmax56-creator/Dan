---
title: Паттерн "Opus планирует, Sonnet исполняет" — снижение стоимости API в CRM-автоматизациях
tags: #biz_recipe #automation #bitrix24 #moysklad #claude_code #cost_optimization #action_needed
---

### 1. Описание идеи
При сложных CRM-задачах (анализ сделки, генерация договора, отчёт по складу) вызов Opus 4.7 на каждое действие дорог. Паттерн: Opus получает задачу один раз и возвращает пошаговый план в JSON. Sonnet 4.6 исполняет каждый шаг плана. Итог: качество мышления Opus при стоимости Sonnet на 80% шагов.

### 2. Технический стек
- AI: Claude API — Opus 4.7 (планирование) + Sonnet 4.6 (исполнение)
- CRM/ERP: Bitrix24 / МойСклад (через REST API)
- Middleware: Python / n8n Function node

### 3. Пошаговый план внедрения
1. При входящем запросе (вебхук Bitrix24 или ручной) — вызвать Opus с системным промптом-планировщиком (код ниже)
2. Opus возвращает JSON-план: список шагов с типом (`api_call`, `generate_text`, `decision`)
3. Итерировать по шагам: `api_call` → прямой HTTP к Bitrix24/МойСклад без AI; `generate_text` → Sonnet; `decision` → Sonnet с коротким промптом
4. Результаты шагов передавать в контекст следующего шага (цепочка)
5. Финальный результат — агрегировать и вернуть в Bitrix24 (`crm.deal.update` / `disk.file.upload`)

### 4. Промпты и Код
```python
import anthropic
import json

client = anthropic.Anthropic()

PLANNER_SYSTEM = """
Ты — архитектор задачи. Получив запрос, верни ТОЛЬКО JSON-массив шагов:
[
  {"step": 1, "type": "api_call", "target": "bitrix24", "action": "crm.deal.get", "params": {"id": 123}},
  {"step": 2, "type": "generate_text", "prompt": "Составь резюме сделки на основе: {step_1_result}"},
  {"step": 3, "type": "api_call", "target": "bitrix24", "action": "crm.deal.update", "params": {"id": 123, "fields": {"COMMENTS": "{step_2_result}"}}}
]
Типы: api_call (без AI), generate_text (Sonnet), decision (Sonnet, ответ: yes/no + reason).
"""

def plan(task: str) -> list:
    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1000,
        system=PLANNER_SYSTEM,
        messages=[{"role": "user", "content": task}]
    )
    return json.loads(resp.content[0].text)

def execute_step(step: dict, context: dict) -> str:
    if step["type"] == "api_call":
        # Прямой вызов API без Claude
        return call_api(step["target"], step["action"], step["params"])
    
    if step["type"] in ("generate_text", "decision"):
        prompt = step["prompt"].format(**context)
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.content[0].text

def run(task: str):
    steps = plan(task)           # 1 вызов Opus
    context = {}
    for step in steps:
        result = execute_step(step, context)
        context[f"step_{step['step']}_result"] = result
    return context
```

```
# Пример задачи для паттерна:
task = """
Сделка #4521 в Bitrix24 перешла в стадию "Договор".
1. Получи данные сделки и переписку
2. Составь текст договора
3. Загрузи договор как файл и прикрепи к сделке
4. Уведоми ответственного
"""
```

### 5. Оценка эффективности
- Сложность: 3/5
- ROI: снижение стоимости API-вызовов на 60–70% при сохранении качества планирования; Opus вызывается 1 раз вместо N

**Ссылки:** [[02_TOOLS/Claude_API]] | [[03_GUIDES/bitrix24_webhooks]] | [[05_BIZ_RECIPES/052_bitrix_ai_contract]]
