# Cloud Ops Control Center

A portfolio-grade cloud operations control plane built with **FastAPI**. It normalizes infrastructure health signals, calculates operational risk, surfaces actionable incidents, and exposes observability endpoints.

## Features
- Fleet-wide health summary and operational risk scoring
- Service health classification from latency, errors, saturation, and availability
- Incident severity classification with remediation recommendations
- Typed Pydantic contracts and OpenAPI documentation
- Prometheus-compatible metrics
- Docker packaging, health checks, GitHub Actions CI, and pytest coverage

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/docs`.

## API
- `GET /health`
- `GET /api/v1/services`
- `GET /api/v1/summary`
- `GET /api/v1/incidents`
- `GET /metrics`

## Architecture
```
Client -> FastAPI -> Ops engine -> telemetry
                         |-> risk classifier
                         |-> incident recommendations
                         |-> Prometheus metrics
```

The repository ships with deterministic demo telemetry so it runs without cloud credentials. The service layer is intentionally clean so adapters for AWS CloudWatch, Azure Monitor, GCP Cloud Monitoring, Kubernetes, or OpenTelemetry can be added later.

## Engineering focus
Designed to be easy to review in an interview while demonstrating production-minded backend practices: separation of concerns, typed models, deterministic business rules, testability, containerization, CI, health checks, and observability.

## License
MIT
