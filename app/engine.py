from __future__ import annotations

from .data import KNOWLEDGE
from .models import PriorityItem, SurvivalAssessmentRequest


def _priority(category: str, urgency: str, reason: str, actions: list[str]) -> dict:
    return {
        "category": category,
        "urgency": urgency,
        "reason": reason,
        "actions": actions,
    }


def assess(req: SurvivalAssessmentRequest) -> dict:
    items: list[dict] = []

    if req.breathing_problem or req.severe_bleeding:
        reason = "A potentially life-threatening medical condition was reported."
        items.append(_priority(
            "medical",
            "critical",
            reason,
            [
                "Contact emergency services or activate an SOS device if possible.",
                "Move away from immediate hazards if it is safe to do so.",
                "For serious external bleeding, apply firm direct pressure with clean material.",
                "Monitor breathing and responsiveness while help is being arranged.",
            ],
        ))
    elif req.injury:
        items.append(_priority(
            "medical",
            "high",
            "An injury was reported.",
            KNOWLEDGE["first_aid"]["steps"],
        ))

    cold_risk = req.temperature_f is not None and req.temperature_f <= 45
    heat_risk = req.temperature_f is not None and req.temperature_f >= 95
    if not req.has_shelter or req.wet_clothing or cold_risk or heat_risk:
        items.append(_priority(
            "shelter",
            "high" if (req.wet_clothing or cold_risk or heat_risk) else "medium",
            "Exposure conditions can become dangerous quickly.",
            KNOWLEDGE["shelter"]["steps"],
        ))

    water_per_day = max(req.people * 3.0, 0.1)
    water_days = req.water_liters / water_per_day
    water_hours = water_days * 24
    if req.hours_without_water >= 12 or water_days < 1:
        items.append(_priority(
            "water",
            "high",
            "Available water is low for the group size or the reported time without water is significant.",
            KNOWLEDGE["water"]["steps"],
        ))

    if req.lost:
        items.append(_priority(
            "navigation",
            "medium",
            "You reported being lost.",
            KNOWLEDGE["navigation"]["steps"],
        ))
        items.append(_priority(
            "signal",
            "medium",
            "Being discoverable can materially improve rescue chances.",
            KNOWLEDGE["signal"]["steps"],
        ))

    food_days = req.food_calories / max(req.people * 2000.0, 1.0)
    if food_days < 1:
        items.append(_priority(
            "food",
            "low",
            "Food reserves are below roughly one day at a planning assumption of 2,000 calories per person.",
            KNOWLEDGE["food"]["steps"],
        ))

    urgency_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    items.sort(key=lambda x: urgency_order[x["urgency"]])

    if not items:
        items.append(_priority(
            "stability",
            "low",
            "No immediate critical shortage or emergency flag was detected.",
            [
                "Maintain shelter, hydration, communications, and situational awareness.",
                "Inventory supplies and identify the next likely failure point.",
                "Preserve power, water, and fuel.",
            ],
        ))

    priorities = [
        PriorityItem(rank=i + 1, **item)
        for i, item in enumerate(items)
    ]

    notes = [
        "Core recommendations are deterministic and work offline.",
        "Water estimate uses a conservative baseline of 3 liters per person per day and does not include all cooking or hygiene needs.",
        "Food estimate uses 2,000 calories per person per day for planning only.",
    ]

    return {
        "status": "critical" if priorities[0].urgency == "critical" else "assessed",
        "priorities": priorities,
        "water_hours_estimate": round(water_hours, 1),
        "food_days_estimate": round(food_days, 2),
        "notes": notes,
    }


def water_requirement_liters(people: int, days: float, hot_weather: bool, strenuous_activity: bool) -> tuple[float, list[str]]:
    liters_per_person_day = 3.0
    assumptions = ["Baseline: 3.0 liters per person per day for drinking/planning."]
    if hot_weather:
        liters_per_person_day += 1.0
        assumptions.append("Added 1.0 liter/person/day for hot-weather planning.")
    if strenuous_activity:
        liters_per_person_day += 1.0
        assumptions.append("Added 1.0 liter/person/day for strenuous-activity planning.")
    return people * days * liters_per_person_day, assumptions


def search_knowledge(query: str) -> list[dict]:
    q = query.lower().strip()
    if not q:
        return []
    results = []
    for topic, item in KNOWLEDGE.items():
        haystack = " ".join([topic, item["summary"], *item["steps"], *item["warnings"]]).lower()
        if q in haystack or any(token in haystack for token in q.split()):
            results.append({"topic": topic, **item})
    return results
