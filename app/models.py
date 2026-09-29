from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class SurvivalAssessmentRequest(BaseModel):
    people: int = Field(default=1, ge=1, le=100)
    hours_without_water: float = Field(default=0, ge=0)
    temperature_f: Optional[float] = None
    injury: bool = False
    severe_bleeding: bool = False
    breathing_problem: bool = False
    lost: bool = False
    has_shelter: bool = True
    wet_clothing: bool = False
    water_liters: float = Field(default=0, ge=0)
    food_calories: float = Field(default=0, ge=0)
    phone_battery_percent: Optional[int] = Field(default=None, ge=0, le=100)


class PriorityItem(BaseModel):
    rank: int
    category: str
    urgency: str
    reason: str
    actions: List[str]


class AssessmentResponse(BaseModel):
    status: str
    priorities: List[PriorityItem]
    water_hours_estimate: Optional[float]
    food_days_estimate: Optional[float]
    notes: List[str]


class WaterPlanRequest(BaseModel):
    people: int = Field(ge=1, le=100)
    days: float = Field(ge=0.25, le=365)
    hot_weather: bool = False
    strenuous_activity: bool = False


class WaterPlanResponse(BaseModel):
    liters: float
    gallons: float
    assumptions: List[str]


class SearchResult(BaseModel):
    topic: str
    summary: str
    steps: List[str]
    warnings: List[str]
