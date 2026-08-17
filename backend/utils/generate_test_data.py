from __future__ import annotations

import argparse
import os
import random
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.database import SessionLocal, init_db
from backend.models.jira_models import JiraBug, JiraSprint, JiraStory, JiraUser
from backend.models.servicenow_models import ServiceNowDeployment, ServiceNowIncident
from backend.models.splunk_models import SplunkLog
from backend.utils.reset_data import reset_demo_data


FIRST_NAMES = ["Avery", "Jordan", "Morgan", "Riley", "Casey", "Taylor", "Cameron", "Parker", "Quinn", "Reese"]
LAST_NAMES = ["Chen", "Patel", "Rivera", "Nguyen", "Wilson", "Kim", "Morgan", "Davis", "Shah", "Brooks"]
STORY_TOPICS = [
    ("payment authorization", "Improve authorization reliability for checkout transactions."),
    ("merchant settlement", "Automate settlement validation and reconciliation."),
    ("fraud review", "Improve risk scoring and manual review workflows."),
    ("refund processing", "Make refund status and retry handling observable."),
    ("ledger reporting", "Improve ledger reporting accuracy for finance operations."),
    ("gateway failover", "Add resilient failover behavior for payment providers."),
]
INCIDENT_TOPICS = [
    ("Payment API latency spike", "Payment API latency exceeded the agreed service threshold."),
    ("Settlement job failure", "The nightly settlement job failed while processing ledger records."),
    ("Fraud scoring timeout", "Fraud scoring responses exceeded the transaction timeout."),
    ("Provider 502 responses", "The downstream payment provider returned intermittent 502 responses."),
    ("Reconciliation mismatch", "Reconciliation detected inconsistent account balances."),
]
LOG_TOPICS = [
    ("payment-service", "ERROR", "Payment gateway timeout after {seconds} seconds.", "payment-service"),
    ("payment-service", "ERROR", "Database connection pool exhausted during authorization.", "payment-service"),
    ("payment-service", "WARN", "Retry queue reached {percent} percent capacity.", "payment-service"),
    ("transaction-api", "ERROR", "Downstream provider returned intermittent 502 responses.", "transaction-api"),
    ("transaction-api", "INFO", "Transaction processing latency reached {latency} milliseconds.", "transaction-api"),
    ("fraud-detection", "ERROR", "Fraud scoring latency exceeded {latency} milliseconds.", "fraud-detection"),
    ("account-service", "ERROR", "Balance mismatch detected during reconciliation.", "account-service"),
]


def _next_number(values: Iterable[str], pattern: str) -> int:
    matcher = re.compile(pattern)
    numbers = [int(match.group(1)) for value in values if (match := matcher.fullmatch(value))]
    return max(numbers, default=0) + 1


def _ensure_users(db) -> list[JiraUser]:
    users = db.query(JiraUser).all()
    for index, (first, last) in enumerate(zip(FIRST_NAMES, LAST_NAMES), start=1):
        username = f"generated_{index:02d}"
        if not any(user.username == username for user in users):
            user = JiraUser(
                username=username,
                full_name=f"{first} {last}",
                email=f"{username}@mahalopay.com",
                role=random.choice(["developer", "qa", "product_manager"]),
            )
            db.add(user)
            users.append(user)
    db.flush()
    return users


def generate_jira_data(db, stories_count: int, bugs_count: int, sprints_count: int) -> dict[str, int]:
    users = _ensure_users(db)
    existing_story_keys = [story.story_key for story in db.query(JiraStory.story_key).all()]
    existing_bug_keys = [bug.bug_key for bug in db.query(JiraBug.bug_key).all()]
    existing_sprint_names = [sprint.sprint_name for sprint in db.query(JiraSprint.sprint_name).all()]
    story_number = _next_number(existing_story_keys, r"STORY-GEN-(\d+)")
    bug_number = _next_number(existing_bug_keys, r"BUG-GEN-(\d+)")
    sprint_number = _next_number(existing_sprint_names, r"Generated Sprint (\d+)")

    generated_sprints = []
    generated_sprint_models = {}
    for offset in range(sprints_count):
        sprint = JiraSprint(
            sprint_name=f"Generated Sprint {sprint_number + offset:03d}",
            goal=random.choice([topic[0].title() for topic in STORY_TOPICS]),
            velocity=random.choice([21, 26, 34, 42]),
            completed_stories=0,
            total_stories=0,
            status=random.choice(["Planned", "Active", "Completed"]),
        )
        db.add(sprint)
        generated_sprints.append(sprint.sprint_name)
        generated_sprint_models[sprint.sprint_name] = sprint

    stories = []
    for offset in range(stories_count):
        topic, description = random.choice(STORY_TOPICS)
        status = random.choices(["Backlog", "In Progress", "Done", "Blocked"], weights=[35, 35, 25, 5])[0]
        sprint = generated_sprints[offset % len(generated_sprints)] if generated_sprints else "Sprint 23"
        story = JiraStory(
            story_key=f"STORY-GEN-{story_number + offset:06d}",
            title=f"{topic.title()} improvement {story_number + offset}",
            description=description,
            assignee_id=random.choice(users).id,
            reporter_id=random.choice(users).id,
            story_points=random.choice([2, 3, 5, 8, 13]),
            priority=random.choice(["Low", "Medium", "High", "Critical"]),
            sprint=sprint,
            status=status,
        )
        db.add(story)
        stories.append(story)

    db.flush()
    for sprint_name in generated_sprints:
        sprint_stories = [story for story in stories if story.sprint == sprint_name]
        sprint = generated_sprint_models[sprint_name]
        sprint.total_stories = len(sprint_stories)
        sprint.completed_stories = sum(story.status == "Done" for story in sprint_stories)

    for offset in range(bugs_count):
        topic, description = random.choice(STORY_TOPICS)
        related_story = random.choice(stories) if stories else None
        db.add(JiraBug(
            bug_key=f"BUG-GEN-{bug_number + offset:06d}",
            title=f"{topic.title()} defect {bug_number + offset}",
            description=f"Defect observed in {description.lower()}",
            assignee_id=random.choice(users).id,
            reporter_id=random.choice(users).id,
            severity=random.choice(["Low", "Medium", "High", "Critical"]),
            status=random.choice(["Open", "In Progress", "Resolved"]),
            related_story_id=related_story.id if related_story else None,
        ))

    return {"stories": stories_count, "bugs": bugs_count, "sprints": sprints_count, "users": len(users)}


def generate_servicenow_data(db, count: int) -> int:
    existing = [item.incident_id for item in db.query(ServiceNowIncident).all()]
    number = _next_number(existing, r"INC-GEN-(\d+)")
    for offset in range(count):
        topic, description = random.choice(INCIDENT_TOPICS)
        db.add(ServiceNowIncident(
            incident_id=f"INC-GEN-{number + offset:06d}",
            title=f"{topic} #{number + offset}",
            description=description,
            severity=random.choice(["Low", "Medium", "High", "Critical"]),
            status=random.choice(["New", "Active", "Monitoring", "Resolved"]),
            assigned_group=random.choice(["Platform Reliability", "Finance Ops", "Payments Engineering", "Fraud Operations"]),
        ))
    return count


def generate_servicenow_deployments(db, count: int) -> int:
    existing = [item.deployment_id for item in db.query(ServiceNowDeployment).all()]
    number = _next_number(existing, r"DEPLOY-GEN-(\d+)")
    features = [
        "Payment gateway failover",
        "Retry policy controls",
        "Fraud scoring optimization",
        "Reconciliation observability",
        "Merchant refund workflow",
    ]
    for offset in range(count):
        db.add(ServiceNowDeployment(
            deployment_id=f"DEPLOY-GEN-{number + offset:06d}",
            feature_name=f"{random.choice(features)} {number + offset}",
            version=f"v{random.randint(1, 4)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            environment=random.choice(["production", "staging"]),
            status=random.choice(["Deployed", "Deployed", "Rolled back"]),
            deployed_by=random.choice(["release-engineering", "platform-release", "payments-team"]),
        ))
    return count


def generate_splunk_data(db, count: int, rng: random.Random) -> int:
    now = datetime.utcnow()
    for _ in range(count):
        source, level, template, service = rng.choice(LOG_TOPICS)
        message = template.format(
            seconds=rng.choice([5, 10, 15, 30, 45]),
            percent=rng.choice([70, 80, 85, 90, 95]),
            latency=rng.choice([500, 1000, 1500, 2000, 3000]),
        )
        db.add(SplunkLog(
            source=source,
            level=level,
            message=message,
            service=service,
            timestamp=now - timedelta(minutes=rng.randint(0, 60 * 24 * 30)),
        ))
    return count


def generate_test_data(
    jira_data: int = 0,
    servicenow_data: int = 0,
    servicenow_deployments: int = 0,
    splunk_data: int = 0,
    jira_stories: int | None = None,
    jira_bugs: int | None = None,
    jira_sprints: int | None = None,
    seed: int = 42,
    reset: bool = False,
) -> dict[str, object]:
    if min(jira_data, servicenow_data, servicenow_deployments, splunk_data) < 0:
        raise ValueError("Record counts cannot be negative")
    random.seed(seed)
    rng = random.Random(seed)
    if reset:
        reset_demo_data()
    init_db()
    db = SessionLocal()
    try:
        story_count = jira_stories if jira_stories is not None else jira_data
        bug_count = jira_bugs if jira_bugs is not None else max(1, jira_data // 5) if jira_data else 0
        sprint_count = jira_sprints if jira_sprints is not None else max(1, jira_data // 10) if jira_data else 0
        result = {
            "jira": generate_jira_data(db, story_count, bug_count, sprint_count),
            "servicenow_incidents": generate_servicenow_data(db, servicenow_data),
            "servicenow_deployments": generate_servicenow_deployments(db, servicenow_deployments),
            "splunk_logs": generate_splunk_data(db, splunk_data, rng),
            "seed": seed,
        }
        db.commit()
        return result
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Add realistic MAHALO test data without deleting existing records.")
    parser.add_argument("--jira-data", type=int, default=0, help="Add N JIRA stories, plus N/5 bugs and N/10 sprints.")
    parser.add_argument("--servicenow-data", type=int, default=0, help="Add N ServiceNow incidents.")
    parser.add_argument("--servicenow-deployments", type=int, default=0, help="Add N ServiceNow deployment records.")
    parser.add_argument("--splunk-data", type=int, default=0, help="Add N Splunk logs.")
    parser.add_argument("--jira-stories", type=int, help="Override the story count from --jira-data.")
    parser.add_argument("--jira-bugs", type=int, help="Override the bug count from --jira-data.")
    parser.add_argument("--jira-sprints", type=int, help="Override the sprint count from --jira-data.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for repeatable values.")
    parser.add_argument("--reset", action="store_true", help="Reset demo data before generating records.")
    args = parser.parse_args()
    result = generate_test_data(**vars(args))
    print(result)


if __name__ == "__main__":
    main()
