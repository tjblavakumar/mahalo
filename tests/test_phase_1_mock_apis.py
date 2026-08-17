from fastapi.testclient import TestClient

from backend.jira.app import app as jira_app
from backend.servicenow.app import app as servicenow_app
from backend.splunk.app import app as splunk_app


def test_jira_health_and_story_flow():
    client = TestClient(jira_app)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

    create_user = client.post(
        "/api/jira/users",
        json={"username": "phase1_user", "full_name": "Phase One User", "email": "phase1@example.com"},
    )
    assert create_user.status_code == 200

    create_story = client.post(
        "/api/jira/stories",
        json={
            "title": "Add ACH transaction support",
            "description": "Support ACH model for payout workflows",
            "assignee_username": "phase1_user",
            "reporter_username": "eve_exec",
            "story_points": 5,
            "priority": "High",
            "sprint": "Sprint 24",
            "status": "In Progress",
        },
    )
    assert create_story.status_code == 200
    story = create_story.json()
    assert "story_key" in story

    detail = client.get(f"/api/jira/stories/{story['story_key']}")
    assert detail.status_code == 200


def test_servicenow_incident_flow():
    client = TestClient(servicenow_app)
    response = client.post(
        "/api/servicenow/incidents",
        json={
            "incident_id": "INC9999999",
            "title": "Phase 1 load incident",
            "description": "Payment API latency spike",
            "severity": "High",
            "status": "Active",
        },
    )
    assert response.status_code == 200
    assert response.json()["incident_id"] == "INC9999999"


def test_splunk_log_search_flow():
    client = TestClient(splunk_app)
    create_log = client.post(
        "/api/splunk/logs",
        json={
            "source": "payment-service",
            "level": "ERROR",
            "message": "Timeout while processing ACH settlement",
            "service": "payment-service",
        },
    )
    assert create_log.status_code == 200
    logs = client.get("/api/splunk/search", params={"query": "ACH settlement"})
    assert logs.status_code == 200
    assert len(logs.json()["items"]) >= 1
