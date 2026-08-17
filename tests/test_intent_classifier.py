from agents.intent_classifier import IntentClassifier


def test_classifier_handles_natural_language_without_keywords():
    classifier = IntentClassifier()

    result = classifier.classify("What should we prioritize next from the production failures?")

    assert result["intent"] == "suggest_features"
    assert result["agents"] == ["JIRA Agent", "Splunk Agent"]


def test_classifier_extracts_story_detail_and_write_confirmation():
    classifier = IntentClassifier()

    detail = classifier.classify("Can QA validate ticket STORY-101?")
    write = classifier.classify("Please save this story to JIRA")

    assert detail["intent"] == "write_test_case"
    assert detail["entities"]["story_key"] == "STORY-101"
    assert write["intent"] == "create_story"
    assert write["requires_confirmation"] is True


def test_classifier_routes_executive_update_to_all_tools():
    result = IntentClassifier().classify("Give me the executive update for MahaloPay")

    assert result["intent"] == "executive_overview"
    assert result["agents"] == ["JIRA Agent", "ServiceNow Agent", "Splunk Agent"]


def test_classifier_handles_greeting_without_agents():
    result = IntentClassifier().classify("hello")

    assert result["intent"] == "greeting"
    assert result["agents"] == []
