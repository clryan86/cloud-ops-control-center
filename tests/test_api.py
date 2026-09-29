from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["offline_core"] is True


def test_assessment_prioritizes_critical_medical_issue():
    response = client.post(
        "/api/v1/assess",
        json={
            "people": 1,
            "severe_bleeding": True,
            "water_liters": 2,
            "food_calories": 3000,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "critical"
    assert body["priorities"][0]["category"] == "medical"


def test_water_plan():
    response = client.post(
        "/api/v1/water-plan",
        json={"people": 2, "days": 3, "hot_weather": False, "strenuous_activity": False},
    )
    assert response.status_code == 200
    assert response.json()["liters"] == 18.0


def test_knowledge_search():
    response = client.get("/api/v1/knowledge", params={"q": "water"})
    assert response.status_code == 200
    assert any(item["topic"] == "water" for item in response.json())
