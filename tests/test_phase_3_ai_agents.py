from agents.context_manager import context_manager
from agents.jira_agent import JiraAgent
from agents.orchestrator import OrchestratorAgent
from agents.servicenow_agent import ServiceNowAgent
from agents.splunk_agent import SplunkAgent


class FakeAgent:
    def __init__(self, source):
        self.source = source

    async def retrieve_context(self, query):
        return {"source": self.source, "success": True, "data": [{"query": query}]}


def test_context_manager_tracks_messages():
    context_manager.clear()
    context_manager.add_message("user", "What is the payment sprint status?")
    context_manager.add_message("assistant", "Sprint 24 is active.")
    history = context_manager.get_conversation_history(last_n=10)
    assert len(history) == 2
    assert history[0]["role"] == "user"


def test_orchestrator_routes_story_queries():
    agent = OrchestratorAgent()
    result = agent.route_query("Show me the payment backlog and story status")
    assert "JIRA" in result


def test_specialized_agents_return_named_response():
    jira = JiraAgent()
    servicenow = ServiceNowAgent()
    splunk = SplunkAgent()

    assert "JIRA" in jira.process_query("Show me payment story status")
    assert "ServiceNow" in servicenow.process_query("Check payment service incident")
    assert "Splunk" in splunk.process_query("Show me payment latency errors")


def test_orchestrator_retrieves_context_from_selected_agents():
    agent = OrchestratorAgent(
        jira_agent=FakeAgent("JIRA"),
        servicenow_agent=FakeAgent("ServiceNow"),
        splunk_agent=FakeAgent("Splunk"),
    )

    import asyncio

    agents_used, contexts = asyncio.run(
        agent.retrieve_context("Explain the payment incident and related error logs")
    )
    assert agents_used == ["ServiceNow Agent", "Splunk Agent"]
    assert [context["source"] for context in contexts] == ["ServiceNow", "Splunk"]


def test_velocity_response_is_human_readable(monkeypatch):
    from backend.config import settings

    class VelocityAgent:
        async def retrieve_context(self, query):
            return {
                "source": "JIRA",
                "success": True,
                "data": {"items": []},
                "summary": {
                    "total_stories": 3,
                    "completed_stories": 1,
                    "in_progress_stories": 1,
                    "backlog_stories": 1,
                    "total_story_points": 26,
                    "completed_story_points": 8,
                    "completion_percent": 30.8,
                },
            }

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(jira_agent=VelocityAgent())
    import asyncio

    response = asyncio.run(agent.process_query("Executive", "show me velocity"))
    assert response == (
        "Executive, the current sprint has completed 8 of 26 story points (30.8%). "
        "That is 1 completed, 1 in progress, and 1 in backlog across 3 stories."
    )


def test_bug_and_assignment_responses_are_complete(monkeypatch):
    from backend.config import settings

    class JiraQueryAgent:
        async def retrieve_context(self, query):
            if "bug" in query.lower():
                return {
                    "source": "JIRA",
                    "record_type": "bugs",
                    "success": True,
                    "data": {"items": [
                        {"bug_key": "BUG-789", "assignee_username": "alice_dev"},
                        {"bug_key": "BUG-102", "assignee_username": "diana_dev"},
                    ]},
                    "summary": {"total_bugs": 2, "critical_bugs": 1, "open_bugs": 2},
                }
            return {
                "source": "JIRA",
                "success": True,
                "data": {"items": [{"story_key": "STORY-103", "assignee_username": "alice_dev"}]},
            }

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(jira_agent=JiraQueryAgent())
    import asyncio

    bug_response = asyncio.run(agent.process_query("Executive", "how many bugs are there and who is working on it"))
    story_response = asyncio.run(agent.process_query("Executive", "who is assigned to story-103"))
    assert "JIRA has 2 bugs" in bug_response
    assert "BUG-789 (alice_dev)" in bug_response
    assert "STORY-103 is assigned to alice_dev" in story_response


def test_product_manager_can_turn_logs_into_story(monkeypatch):
    from backend.config import settings

    class ScenarioAgent:
        def __init__(self, source, items):
            self.source = source
            self.items = items

        async def retrieve_context(self, query):
            return {"source": self.source, "success": True, "data": {"items": self.items}}

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(
        jira_agent=ScenarioAgent("JIRA", []),
        splunk_agent=ScenarioAgent("Splunk", [
            {"message": "Payment gateway timeout after 30 seconds"},
            {"message": "Database connection pool exhausted"},
        ]),
    )
    import asyncio

    response = asyncio.run(agent.process_query(
        "Product Manager",
        "based on the logs, help me create a user story to fix it",
    ))
    assert "Improve payment gateway timeout recovery" in response
    assert "Payment gateway timeout" in response
    assert "Acceptance criteria" in response


def test_error_count_uses_splunk_level(monkeypatch):
    from backend.config import settings

    class SplunkQueryAgent:
        async def retrieve_context(self, query):
            return {
                "source": "Splunk",
                "record_type": "error_logs",
                "success": True,
                "data": {"items": [
                    {"id": 1, "level": "ERROR", "message": "Gateway timeout"},
                    {"id": 2, "level": "ERROR", "message": "Pool exhausted"},
                ]},
                "summary": {"error_count": 2},
            }

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(splunk_agent=SplunkQueryAgent())
    import asyncio

    response = asyncio.run(agent.process_query("Product Manager", "how many errors are in the logs now"))
    assert response == "Product Manager, Splunk contains 2 error logs."


def test_story_suggestions_use_error_logs(monkeypatch):
    from backend.config import settings

    class SplunkQueryAgent:
        async def retrieve_context(self, query):
            return {
                "source": "Splunk",
                "success": True,
                "data": {"items": [
                    {"id": 1, "level": "ERROR", "message": "Payment gateway timeout"},
                    {"id": 2, "level": "ERROR", "message": "Connection pool exhausted"},
                ]},
                "record_type": "error_logs",
                "summary": {"error_count": 2},
            }

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(splunk_agent=SplunkQueryAgent())
    import asyncio

    response = asyncio.run(agent.process_query("Product Manager", "suggest few user stories based on errors in logs"))
    assert "three user stories" in response
    assert "Improve payment gateway timeout recovery" in response
    assert "Acceptance criteria" in response


def test_log_analysis_recommends_missing_stories(monkeypatch):
    from backend.config import settings

    class QueryAgent:
        def __init__(self, source, items):
            self.source = source
            self.items = items

        async def retrieve_context(self, query):
            return {"source": self.source, "success": True, "data": {"items": self.items}}

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(
        jira_agent=QueryAgent("JIRA", [{"title": "Payment gateway integration", "description": "Checkout support"}]),
        splunk_agent=QueryAgent("Splunk", [
            {"level": "ERROR", "message": "Payment gateway timeout and provider 502"},
            {"level": "ERROR", "message": "Connection pool exhausted during retry"},
        ]),
    )
    import asyncio

    response = asyncio.run(agent.process_query("Product Manager", "analyze the logs and tell me if I need to create more user stories"))
    assert "yes" in response.lower()
    assert "gateway timeout" in response.lower()
    assert "retry backoff" in response.lower()


def test_follow_up_elaborates_and_explicitly_writes_story(monkeypatch):
    from backend.config import settings

    class FakeJira:
        def __init__(self):
            self.created = None

        async def retrieve_context(self, query):
            return {"source": "JIRA", "success": True, "data": {"items": []}}

        async def create_story(self, story):
            self.created = story
            return {"success": True, "data": {"story_key": "STORY-GEN-900001"}}

    class FakeSplunk:
        async def retrieve_context(self, query):
            return {"source": "Splunk", "success": True, "data": {"items": [
                {"level": "ERROR", "message": "Payment gateway timeout"},
            ]}}

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    jira = FakeJira()
    agent = OrchestratorAgent(jira_agent=jira, splunk_agent=FakeSplunk())
    import asyncio

    asyncio.run(agent.process_query("Product Manager", "analyze the logs and tell me if I need to create more user stories"))
    draft = asyncio.run(agent.process_query("Product Manager", "ok help me create the suggested use case with complete details including acceptance criteria"))
    assert "complete JIRA story draft" in draft
    assert "Acceptance criteria" in draft
    assert "Payment gateway timeout" in draft
    assert jira.created is None

    created = asyncio.run(agent.process_query("Product Manager", "create this story in JIRA"))
    assert "STORY-GEN-900001" in created
    assert jira.created["title"]


def test_review_request_does_not_create_until_confirmation(monkeypatch):
    from backend.config import settings

    class FakeJira:
        def __init__(self):
            self.created = []

        async def retrieve_context(self, query):
            return {"source": "JIRA", "success": True, "data": {"items": []}}

        async def create_story(self, story):
            self.created.append(story)
            return {"success": True, "data": {"story_key": f"STORY-GEN-{len(self.created):06d}"}}

    class FakeSplunk:
        async def retrieve_context(self, query):
            return {"source": "Splunk", "success": True, "data": {"items": [
                {"level": "ERROR", "message": "Payment gateway timeout"},
                {"level": "ERROR", "message": "Connection pool exhausted during retry"},
            ]}}

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    jira = FakeJira()
    agent = OrchestratorAgent(jira_agent=jira, splunk_agent=FakeSplunk())
    import asyncio

    asyncio.run(agent.process_query("Product Manager", "help me analyze logs and suggest user stories"))
    review = asyncio.run(agent.process_query(
        "Product Manager",
        "ok. help me create these user stories. let me review it first before you create actual jira story",
    ))
    assert "story drafts" in review
    assert "No stories have been created yet" in review
    assert jira.created == []

    created = asyncio.run(agent.process_query("Product Manager", "create these stories in JIRA"))
    assert "created 2 stories" in created
    assert len(jira.created) == 2


def test_elaborate_first_suggested_story_uses_pending_draft(monkeypatch):
    from backend.config import settings

    class QueryAgent:
        async def retrieve_context(self, query):
            return {"source": "Splunk", "success": True, "data": {"items": [
                {"level": "ERROR", "message": "Payment gateway timeout"},
                {"level": "ERROR", "message": "Connection pool exhausted during retry"},
            ]}}

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(splunk_agent=QueryAgent())
    import asyncio

    asyncio.run(agent.process_query("Executive", "check the logs for errors and suggest user stories to fix them"))
    response = asyncio.run(agent.process_query("Executive", "can you elaborate the 1st user story with more details"))
    assert "Improve payment gateway timeout recovery" in response
    assert "Payment gateway timeouts use bounded retries" in response
    assert "No stories have been created yet" not in response


def test_elaborate_named_suggested_story_and_explain_priority(monkeypatch):
    from backend.config import settings

    class QueryAgent:
        async def retrieve_context(self, query):
            return {"source": "Splunk", "success": True, "data": {"items": [
                {"level": "ERROR", "message": "Payment gateway timeout"},
                {"level": "ERROR", "message": "Fraud scoring latency exceeded target"},
                {"level": "ERROR", "message": "Balance mismatch detected during reconciliation"},
            ]}}

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(splunk_agent=QueryAgent())
    import asyncio

    asyncio.run(agent.process_query("Executive", "check the logs for errors and suggest user stories to fix them"))
    response = asyncio.run(agent.process_query(
        "Executive",
        'elaborate "title: Reduce fraud and reconciliation processing latency" why is it priority',
    ))
    assert "Reduce fraud and reconciliation processing latency" in response
    assert "Medium priority" in response
    assert "gateway timeout recovery" not in response


def test_story_test_case_uses_requested_story_detail(monkeypatch):
    from backend.config import settings

    class JiraDetailAgent:
        async def retrieve_context(self, query):
            return {
                "source": "JIRA",
                "record_type": "story_detail",
                "success": True,
                "data": {
                    "story_key": "STORY-8",
                    "title": "Improve payment gateway timeout recovery",
                    "description": "Handle provider timeouts and failover.",
                },
            }

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(jira_agent=JiraDetailAgent())
    import asyncio

    response = asyncio.run(agent.process_query("Executive", "help me to write a test case for story 8"))
    assert "STORY-8" in response
    assert "Preconditions" in response
    assert "Expected results" in response
    assert "JIRA found" not in response


def test_missing_story_test_case_explains_how_to_recover(monkeypatch):
    from backend.config import settings

    class MissingJira:
        async def retrieve_context(self, query):
            return {
                "source": "JIRA",
                "record_type": "story_detail",
                "story_key": "STORY-8",
                "success": False,
                "error": "Story not found",
            }

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(jira_agent=MissingJira())
    import asyncio

    response = asyncio.run(agent.process_query("Executive", "help me write a test case for story 8"))
    assert "STORY-8" in response
    assert "STORY-101" in response
    assert "could not find" in response.lower()


def test_production_deployment_count_uses_servicenow(monkeypatch):
    from backend.config import settings

    class DeploymentAgent:
        async def retrieve_context(self, query):
            return {
                "source": "ServiceNow",
                "record_type": "deployments",
                "success": True,
                "data": {"items": [
                    {"feature_name": "Payments", "version": "v2.4.0"},
                    {"feature_name": "Fraud detection", "version": "v1.8.2"},
                ]},
            }

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(servicenow_agent=DeploymentAgent())
    import asyncio

    response = asyncio.run(agent.process_query("Executive", "how many features are deployed in the production"))
    assert "2 features are deployed in production" in response
    assert "Payments (v2.4.0)" in response


def test_next_feature_from_error_logs_is_answered(monkeypatch):
    from backend.config import settings

    class SplunkAgent:
        async def retrieve_context(self, query):
            return {
                "source": "Splunk",
                "success": True,
                "data": {"items": [
                    {"level": "ERROR", "message": "Payment gateway timeout"},
                    {"level": "ERROR", "message": "Provider returned 502"},
                ]},
            }

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(splunk_agent=SplunkAgent())
    import asyncio

    response = asyncio.run(agent.process_query("Executive", "based on the error logs what is the next feature we should focus"))
    assert "payment gateway timeout recovery and provider failover" in response
    assert "2 error logs" in response


def test_executive_update_combines_all_tools(monkeypatch):
    from backend.config import settings

    class Agent:
        def __init__(self, source, data): self.source, self.data = source, data
        async def retrieve_context(self, query): return {"source": self.source, "success": True, "data": self.data}

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(
        jira_agent=Agent("JIRA", {"items": [{"status": "Done"}]}),
        servicenow_agent=Agent("ServiceNow", {"deployments": [{"feature_name": "Payments"}], "incidents": [{"status": "Active"}]}),
        splunk_agent=Agent("Splunk", {"items": [{"level": "ERROR"}]}),
    )
    import asyncio
    response = asyncio.run(agent.process_query("Executive", "give me the executive update of mahalopay"))
    assert "MahaloPay executive update" in response
    assert "deployed features" in response
    assert "error logs" in response


def test_greeting_does_not_query_tools(monkeypatch):
    from backend.config import settings

    class FailingAgent:
        async def retrieve_context(self, query):
            raise AssertionError("tools should not be queried for greetings")

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(
        jira_agent=FailingAgent(),
        servicenow_agent=FailingAgent(),
        splunk_agent=FailingAgent(),
    )
    import asyncio

    response = asyncio.run(agent.process_query("Executive", "hello"))
    assert "Hello, Executive" in response


def test_compound_error_feature_query_includes_capacity(monkeypatch):
    from backend.config import settings

    class QueryAgent:
        def __init__(self, source, context):
            self.source = source
            self.context = context

        async def retrieve_context(self, query):
            return {"source": self.source, "success": True, **self.context}

    monkeypatch.setattr(settings, "ONE_MIN_AI_API_KEY", "")
    agent = OrchestratorAgent(
        jira_agent=QueryAgent("JIRA", {
            "data": {"items": [{"title": "Payment gateway integration", "description": "Checkout support"}]},
            "summary": {"completed_story_points": 21, "total_story_points": 56},
        }),
        splunk_agent=QueryAgent("Splunk", {
            "data": {"items": [
                {"level": "ERROR", "message": "Payment gateway timeout and provider 502"},
                {"level": "ERROR", "message": "Connection pool exhausted during retry"},
            ]},
        }),
    )
    import asyncio

    response = asyncio.run(agent.process_query(
        "Executive",
        "based on the errors what new feature do we need to build? do we have enough velocity to achieve it in 1 quarter?",
    ))
    assert "gateway timeout recovery" in response
    assert "quarter" in response
    assert "enough capacity" in response
