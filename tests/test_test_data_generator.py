from backend.database import SessionLocal
from backend.models.jira_models import JiraBug, JiraSprint, JiraStory
from backend.models.servicenow_models import ServiceNowDeployment, ServiceNowIncident
from backend.models.splunk_models import SplunkLog
from backend.utils.generate_test_data import generate_test_data


def test_generator_adds_requested_record_volumes():
    result = generate_test_data(
        jira_data=4,
        servicenow_data=3,
        servicenow_deployments=4,
        splunk_data=6,
        seed=7,
    )

    assert result["jira"]["stories"] == 4
    assert result["servicenow_incidents"] == 3
    assert result["servicenow_deployments"] == 4
    assert result["splunk_logs"] == 6

    with SessionLocal() as db:
        assert db.query(JiraStory).filter(JiraStory.story_key.like("STORY-GEN-%")).count() >= 4
        assert db.query(JiraBug).filter(JiraBug.bug_key.like("BUG-GEN-%")).count() >= 1
        assert db.query(JiraSprint).filter(JiraSprint.sprint_name.like("Generated Sprint %")).count() >= 1
        assert db.query(ServiceNowIncident).filter(ServiceNowIncident.incident_id.like("INC-GEN-%")).count() >= 3
        assert db.query(ServiceNowDeployment).filter(ServiceNowDeployment.deployment_id.like("DEPLOY-GEN-%")).count() >= 4
        assert db.query(SplunkLog).count() >= 6
