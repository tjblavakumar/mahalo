from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_root_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_chat_personas():
    response = client.get("/api/chat/personas")
    assert response.status_code == 200
    assert response.json()["count"] >= 4
