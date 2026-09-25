from enum import Enum
from pydantic import BaseModel, Field

class Status(str, Enum):
    healthy = "healthy"
    degraded = "degraded"
    critical = "critical"

class ServiceTelemetry(BaseModel):
    name: str
    region: str
    latency_ms: float = Field(ge=0)
    error_rate: float = Field(ge=0, le=1)
    cpu_percent: float = Field(ge=0, le=100)
    memory_percent: float = Field(ge=0, le=100)
    availability: float = Field(ge=0, le=100)

class ServiceHealth(ServiceTelemetry):
    status: Status
    risk_score: int = Field(ge=0, le=100)

class Incident(BaseModel):
    service: str
    severity: str
    reason: str
    recommendation: str
