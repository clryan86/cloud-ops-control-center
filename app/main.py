from fastapi import FastAPI, Query

from .engine import assess, search_knowledge, water_requirement_liters
from .models import (
    AssessmentResponse,
    SearchResult,
    SurvivalAssessmentRequest,
    WaterPlanRequest,
    WaterPlanResponse,
)

app = FastAPI(
    title="Survival AI",
    version="0.1.0",
    description="Offline-first survival planning and emergency-priority assistant.",
)


@app.get("/")
def root() -> dict:
    return {
        "name": "Survival AI",
        "version": "0.1.0",
        "offline_core": True,
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "offline_core": True}


@app.post("/api/v1/assess", response_model=AssessmentResponse)
def survival_assessment(payload: SurvivalAssessmentRequest) -> AssessmentResponse:
    return AssessmentResponse(**assess(payload))


@app.post("/api/v1/water-plan", response_model=WaterPlanResponse)
def water_plan(payload: WaterPlanRequest) -> WaterPlanResponse:
    liters, assumptions = water_requirement_liters(
        payload.people,
        payload.days,
        payload.hot_weather,
        payload.strenuous_activity,
    )
    return WaterPlanResponse(
        liters=round(liters, 2),
        gallons=round(liters / 3.785411784, 2),
        assumptions=assumptions,
    )


@app.get("/api/v1/knowledge", response_model=list[SearchResult])
def knowledge_search(q: str = Query(min_length=1, max_length=200)) -> list[SearchResult]:
    return [SearchResult(**item) for item in search_knowledge(q)]
