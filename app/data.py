from .models import ServiceTelemetry

DEMO_TELEMETRY = [
    ServiceTelemetry(name="api-gateway", region="us-east-1", latency_ms=82, error_rate=.004, cpu_percent=44, memory_percent=57, availability=99.99),
    ServiceTelemetry(name="billing-worker", region="us-east-1", latency_ms=510, error_rate=.081, cpu_percent=91, memory_percent=88, availability=99.71),
    ServiceTelemetry(name="identity-service", region="us-west-2", latency_ms=225, error_rate=.021, cpu_percent=72, memory_percent=79, availability=99.94),
    ServiceTelemetry(name="event-processor", region="us-west-2", latency_ms=96, error_rate=.006, cpu_percent=52, memory_percent=61, availability=99.98),
]
