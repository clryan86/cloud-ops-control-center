from .models import Incident, ServiceHealth, ServiceTelemetry, Status

def risk_score(t: ServiceTelemetry) -> int:
    latency = min(t.latency_ms / 10, 30)
    errors = min(t.error_rate * 500, 35)
    saturation = max(t.cpu_percent - 70, 0) * 0.6 + max(t.memory_percent - 75, 0) * 0.5
    availability = max(99.9 - t.availability, 0) * 40
    return min(100, round(latency + errors + saturation + availability))

def classify(t: ServiceTelemetry) -> ServiceHealth:
    score = risk_score(t)
    status = Status.critical if score >= 70 else Status.degraded if score >= 35 else Status.healthy
    return ServiceHealth(**t.model_dump(), status=status, risk_score=score)

def incident_for(h: ServiceHealth) -> Incident | None:
    if h.status == Status.healthy:
        return None
    reasons, actions = [], []
    if h.error_rate >= .05:
        reasons.append(f"error rate {h.error_rate:.1%}")
        actions.append("inspect recent deploys and upstream dependency failures")
    if h.latency_ms >= 300:
        reasons.append(f"latency {h.latency_ms:.0f}ms")
        actions.append("profile slow requests and validate downstream latency")
    if h.cpu_percent >= 85 or h.memory_percent >= 90:
        reasons.append("resource saturation")
        actions.append("scale capacity and inspect hot processes")
    if h.availability < 99.9:
        reasons.append(f"availability {h.availability:.2f}%")
        actions.append("review failed health checks and regional dependencies")
    return Incident(service=h.name, severity="SEV-1" if h.status == Status.critical else "SEV-2", reason=", ".join(reasons) or "composite operational risk", recommendation="; ".join(dict.fromkeys(actions)) or "inspect telemetry and recent changes")
