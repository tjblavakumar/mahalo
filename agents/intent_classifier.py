from __future__ import annotations

import json
import re
from typing import Any

from litellm import completion

from backend.config import settings


INTENT_SCHEMA = {
    "intent": "One of: greeting, executive_overview, analyze_errors, suggest_features, count_deployments, check_velocity, story_detail, create_story, write_test_case, incident_status, general_sdlc",
    "agents": ["JIRA Agent", "ServiceNow Agent", "Splunk Agent"],
    "entities": {"story_key": "optional STORY-* key", "environment": "optional environment"},
    "requires_confirmation": False,
}


class IntentClassifier:
    def classify(self, query: str) -> dict[str, Any]:
        normalized = query.lower()
        fallback = self._fallback(normalized)
        if not settings.ONE_MIN_AI_API_KEY:
            return fallback
        try:
            response = completion(
                model=settings.LITELLM_MODEL,
                api_key=settings.ONE_MIN_AI_API_KEY,
                base_url=settings.ONE_MIN_AI_BASE_URL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Classify the user request for MAHALO SDLC orchestration. Return JSON only. "
                            "Never authorize a write; set requires_confirmation true for create/save/write actions. "
                            f"Schema example: {json.dumps(INTENT_SCHEMA)}"
                        ),
                    },
                    {"role": "user", "content": query},
                ],
                temperature=0,
                max_tokens=180,
            )
            parsed = json.loads(response.choices[0].message.content)
            validated = self._validate(parsed, fallback)
            if validated.get("intent") == "general_sdlc" and fallback.get("intent") != "general_sdlc":
                return fallback
            return validated
        except Exception:
            return fallback

    def _validate(self, result: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
        allowed = {
            "analyze_errors", "suggest_features", "count_deployments", "check_velocity",
            "story_detail", "create_story", "write_test_case", "incident_status", "executive_overview", "greeting", "general_sdlc",
        }
        if result.get("intent") not in allowed:
            return fallback
        result["agents"] = [agent for agent in result.get("agents", []) if agent in INTENT_SCHEMA["agents"]]
        result.setdefault("entities", {})
        result["requires_confirmation"] = bool(result.get("requires_confirmation", False))
        if result["intent"] == "create_story":
            result["requires_confirmation"] = True
        return result

    def _fallback(self, query: str) -> dict[str, Any]:
        story_match = re.search(r"\bstory[- ]?(\d+)\b", query)
        story_key = f"STORY-{story_match.group(1)}" if story_match else None
        if query.strip(" !?,.") in {"hi", "hello", "hey", "good morning", "good afternoon", "good evening"}:
            return self._result("greeting", [])
        if any(term in query for term in ("executive update", "executive summary", "executive overview", "overall update", "overall status")):
            return self._result("executive_overview", ["JIRA Agent", "ServiceNow Agent", "Splunk Agent"])
        if any(term in query for term in ("write a test", "test case", "qa test", "validate")):
            return self._result("write_test_case", ["JIRA Agent"], story_key=story_key)
        if story_key:
            return self._result("story_detail", ["JIRA Agent"], story_key=story_key)
        if any(term in query for term in ("create", "save", "write", "add")) and "story" in query:
            return self._result("create_story", ["JIRA Agent", "Splunk Agent"], requires_confirmation=True)
        if "deploy" in query or ("production" in query and "feature" in query):
            return self._result("count_deployments", ["ServiceNow Agent"], environment="production")
        if any(term in query for term in ("suggest", "recommend", "next feature", "focus", "prioritize")) and any(term in query for term in ("error", "log", "feature", "failure", "production")):
            return self._result("suggest_features", ["JIRA Agent", "Splunk Agent"])
        if any(term in query for term in ("error", "errors", "failure", "failures", "production failures")) and any(term in query for term in ("feature", "story", "stories", "next", "focus", "logs", "quarter")):
            return self._result("analyze_errors", ["JIRA Agent", "Splunk Agent"])
        if "velocity" in query and any(term in query for term in ("quarter", "sprint", "story", "feature")):
            return self._result("check_velocity", ["JIRA Agent"])
        if any(term in query for term in ("analyze", "analyse", "based on")) and any(term in query for term in ("error", "log", "story", "feature")):
            return self._result("analyze_errors", ["JIRA Agent", "Splunk Agent"])
        if "incident" in query or "outage" in query:
            return self._result("incident_status", ["ServiceNow Agent"])
        return self._result("general_sdlc", ["JIRA Agent", "ServiceNow Agent", "Splunk Agent"])

    @staticmethod
    def _result(intent: str, agents: list[str], story_key: str | None = None, environment: str | None = None, requires_confirmation: bool = False) -> dict[str, Any]:
        entities: dict[str, Any] = {}
        if story_key:
            entities["story_key"] = story_key
        if environment:
            entities["environment"] = environment
        return {
            "intent": intent,
            "agents": agents,
            "entities": entities,
            "requires_confirmation": requires_confirmation,
        }
