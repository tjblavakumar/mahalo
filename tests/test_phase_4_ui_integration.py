from fastapi.testclient import TestClient

from api.main import app
from api.routes import chat


async def fake_process_query(user_persona, user_query, conversation_history=None):
    return f"Handled by MAHALO for {user_persona}: {user_query}"


def test_gateway_contract(monkeypatch):
    monkeypatch.setattr(chat.orchestrator, "process_query", fake_process_query)
    chat.context_manager.clear()
    client = TestClient(app)

    assert client.get("/").json()["frontend"] == "http://localhost:3000"
    assert client.get("/health").json()["status"] == "healthy"
    assert client.get("/api/chat/personas").json()["count"] == 4

    response = client.post(
        "/api/chat/message",
        json={"persona": "QA", "message": "Show payment errors"},
    )
    assert response.status_code == 200
    assert response.json()["agents_used"] == ["Splunk Agent"]

    stats = client.get("/api/admin/stats")
    assert stats.json()["conversations"]["total_messages"] == 2


def test_admin_reset_clears_context():
    client = TestClient(app)
    response = client.post("/api/admin/reset-data")
    assert response.status_code == 200
    assert client.get("/api/admin/stats").json()["conversations"]["total_messages"] == 0
