# Survival AI

Offline-first survival planning assistant built with FastAPI.

Survival AI is designed to remain useful when internet access is weak or unavailable. It combines a local knowledge base, emergency triage rules, inventory-aware planning, and a clean API that can later be connected to a local LLM.

## Current capabilities

- Emergency priority assessment: immediate danger, water, shelter, temperature, food, navigation and communications
- Offline survival knowledge library with searchable topics
- 72-hour plan generator
- Water requirement calculator
- Food/calorie planning calculator
- Inventory-aware recommendations
- Basic location/context fields without requiring cloud services
- Deterministic responses that work without an AI API key
- Optional local-model integration point
- FastAPI/OpenAPI interface
- Pytest-ready architecture

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:
- App/API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Example

POST `/api/v1/assess`

```json
{
  "people": 2,
  "hours_without_water": 10,
  "temperature_f": 38,
  "injury": false,
  "lost": true,
  "has_shelter": false,
  "water_liters": 1.5,
  "food_calories": 2600
}
```

The response ranks needs and produces a practical action sequence.

## Design principle

This project does not depend on internet connectivity for its core reasoning. The deterministic engine is the safety baseline. A local language model can be added later for conversational responses while keeping the rules engine as the source of truth.

## Safety

This software is educational and planning-oriented. For life-threatening emergencies, contact emergency services when available. Medical guidance is intentionally conservative and does not replace professional care.

## Roadmap

- Local SQLite persistence
- Downloadable regional knowledge packs
- Map and compass tools
- Weather radio / alert ingestion
- Offline local LLM adapter (Ollama / llama.cpp)
- PWA/mobile client
- Encrypted family profiles and go-bag inventories
- Scenario simulator and training mode
- Unit and integration test suite

MIT License.
