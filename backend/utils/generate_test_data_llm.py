"""
Enhanced test data generation using LLM to create realistic, diverse, and contextual data.
This eliminates duplicates and generates rich descriptions with proper context.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import httpx

from backend.config import settings
from backend.database import SessionLocal, init_db
from backend.models.jira_models import JiraBug, JiraSprint, JiraStory, JiraUser
from backend.models.servicenow_models import ServiceNowDeployment, ServiceNowIncident
from backend.models.splunk_models import SplunkLog
from backend.utils.reset_data import reset_demo_data


class LLMTestDataGenerator:
    """Generate realistic test data using LLM for better variety and context."""
    
    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)
        self.api_key = settings.ONE_MIN_AI_API_KEY
        self.model = settings.LITELLM_MODEL
        self.generated_keys = set()

    async def _chat(self, prompt: str, temperature: float = 0.9) -> str:
        """Call 1min.ai Chat with AI endpoint and return the text result."""
        payload = {
            "type": "UNIFY_CHAT_WITH_AI",
            "model": self.model,
            "promptObject": {
                "prompt": prompt,
                "settings": {
                    "withMemories": False,
                    "historySettings": {"isMixed": False, "historyMessageLimit": 10},
                    "webSearchSettings": {"maxWord": 1000, "numOfSite": 3, "webSearch": False},
                },
                "attachments": {"files": [], "images": []},
            },
        }
        async with httpx.AsyncClient(timeout=120.0, trust_env=True) as client:
            response = await client.post(
                "https://api.1min.ai/api/chat-with-ai",
                headers={"Content-Type": "application/json", "API-KEY": self.api_key},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        result_list = data.get("aiRecord", {}).get("aiRecordDetail", {}).get("resultObject", [])
        return result_list[0] if result_list else ""

    def _parse_json(self, content: str) -> list[dict[str, Any]]:
        """Extract and parse a JSON array from LLM text output."""
        content = content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    
    async def generate_user_profiles(self, count: int) -> list[dict[str, Any]]:
        """Generate diverse user profiles with realistic names and roles."""
        prompt = f"""Generate {count} diverse employee profiles for a fintech payment processing company.
        
Return ONLY a JSON array with this exact structure:
[
  {{"first_name": "...", "last_name": "...", "role": "developer|qa|product_manager|devops|security", "email_prefix": "..."}}
]

Requirements:
- Diverse names from different cultures
- Realistic roles matching fintech/payments domain
- Email prefix should be firstname.lastname format
- No duplicate names
"""
        content = await self._chat(prompt)
        return self._parse_json(content)
    
    async def generate_jira_stories(
        self, 
        count: int, 
        existing_keys: list[str],
        users: list[JiraUser]
    ) -> list[dict[str, Any]]:
        """Generate diverse JIRA stories with rich context."""
        prompt = f"""Generate {count} unique JIRA user stories for a payment processing platform (similar to Stripe).

Context: The platform handles payment authorization, fraud detection, merchant settlement, refunds, ledger management, and gateway integration.

Return ONLY a JSON array with this exact structure:
[
  {{
    "title": "Brief user story title (max 100 chars)",
    "description": "Detailed user story with acceptance criteria, technical context, and business value (150-300 words)",
    "story_points": 2|3|5|8|13,
    "priority": "Low|Medium|High|Critical",
    "status": "Backlog|In Progress|Done|Blocked",
    "topic_area": "payment|fraud|settlement|refunds|ledger|gateway"
  }}
]

Requirements:
- Each story should be unique and realistic
- Include acceptance criteria in description
- Add technical context where relevant
- Mention specific payment scenarios (e.g., 3DS, SCA, PSD2)
- No generic or duplicate stories
- Focus on real fintech payment challenges
"""
        content = await self._chat(prompt)
        return self._parse_json(content)
    
    async def generate_jira_bugs(
        self, 
        count: int,
        existing_keys: list[str],
        stories: list[JiraStory],
        users: list[JiraUser]
    ) -> list[dict[str, Any]]:
        """Generate realistic bug reports with detailed reproduction steps."""
        prompt = f"""Generate {count} realistic bug reports for a payment processing platform.

Return ONLY a JSON array with this exact structure:
[
  {{
    "title": "Brief bug title describing the issue",
    "description": "Detailed bug description including: reproduction steps, expected behavior, actual behavior, impact, environment details (200-300 words)",
    "severity": "Low|Medium|High|Critical",
    "status": "Open|In Progress|Resolved",
    "topic_area": "payment|fraud|settlement|refunds|ledger|gateway|api|database"
  }}
]

Requirements:
- Realistic payment system bugs (timeouts, data inconsistencies, race conditions, etc.)
- Clear reproduction steps
- Mention specific error codes or logs where appropriate
- Include impact on business/customers
- Technical details (database locks, API errors, network issues, etc.)
"""
        content = await self._chat(prompt)
        return self._parse_json(content)
    
    async def generate_servicenow_incidents(
        self, 
        count: int,
        existing_keys: list[str]
    ) -> list[dict[str, Any]]:
        """Generate realistic incident reports."""
        prompt = f"""Generate {count} realistic production incidents for a payment processing platform.

Return ONLY a JSON array with this exact structure:
[
  {{
    "title": "Brief incident title",
    "description": "Detailed incident description including: timeline, impact, affected services, metrics, resolution steps (200-400 words)",
    "severity": "Low|Medium|High|Critical",
    "status": "New|Active|Monitoring|Resolved",
    "assigned_group": "Platform Reliability|Payments Engineering|Fraud Operations|Database Team|Network Operations"
  }}
]

Requirements:
- Realistic production incidents (outages, performance degradation, data issues)
- Include specific metrics (latency, error rates, affected transactions)
- Mention SLO/SLA impact
- Include detection method (alerts, customer reports, monitoring)
- Add mitigation/resolution steps taken
"""
        content = await self._chat(prompt)
        return self._parse_json(content)
    
    async def generate_splunk_logs(
        self, 
        count: int
    ) -> list[dict[str, Any]]:
        """Generate realistic log entries with proper context."""
        prompt = f"""Generate {count} realistic log entries for a payment processing platform.

Return ONLY a JSON array with this exact structure:
[
  {{
    "source": "payment-service|fraud-detection|transaction-api|account-service|gateway-connector|settlement-worker",
    "level": "ERROR|WARN|INFO",
    "message": "Detailed log message with context, IDs, metrics, stack traces where appropriate (100-200 chars)",
    "service": "same as source"
  }}
]

Requirements:
- Realistic payment system logs (errors, warnings, performance metrics)
- Include transaction IDs, correlation IDs, timestamps in message
- For errors: include error codes, retry attempts, failure reasons
- For warnings: include threshold values, queue depths, latency numbers
- Use actual technical terminology (circuit breaker, retry policy, connection pool, etc.)
"""
        content = await self._chat(prompt)
        return self._parse_json(content)
    
    async def generate_deployments(
        self,
        count: int,
        existing_keys: list[str]
    ) -> list[dict[str, Any]]:
        """Generate realistic deployment records."""
        prompt = f"""Generate {count} realistic deployment records for a payment processing platform.

Return ONLY a JSON array with this exact structure:
[
  {{
    "feature_name": "Brief feature/fix name",
    "version": "v1.2.3",
    "environment": "production|staging",
    "status": "Deployed|Rolled back",
    "deployed_by": "team name"
  }}
]

Requirements:
- Realistic feature names for payment platform
- Proper semantic versioning
- Mix of features, bug fixes, and infrastructure changes
"""
        content = await self._chat(prompt, temperature=0.8)
        return self._parse_json(content)


async def generate_enhanced_test_data(
    jira_stories: int = 0,
    jira_bugs: int = 0,
    jira_sprints: int = 0,
    servicenow_incidents: int = 0,
    servicenow_deployments: int = 0,
    splunk_logs: int = 0,
    seed: int = 42,
    reset: bool = False,
) -> dict[str, Any]:
    """Generate enhanced test data using LLM."""

    if reset:
        reset_demo_data()

    init_db()
    db = SessionLocal()
    generator = LLMTestDataGenerator(seed=seed)

    try:
        result = {
            "jira_stories": 0,
            "jira_bugs": 0,
            "jira_sprints": 0,
            "servicenow_incidents": 0,
            "servicenow_deployments": 0,
            "splunk_logs": 0,
            "users": 0,
        }

        # Generate users if needed
        existing_users = db.query(JiraUser).all()
        users = existing_users

        if jira_stories > 0 or jira_bugs > 0:
            users_needed = max(10, len(existing_users))
            if len(existing_users) < users_needed:
                print(f"Generating {users_needed - len(existing_users)} new users...")
                user_profiles = await generator.generate_user_profiles(users_needed - len(existing_users))
                
                for profile in user_profiles:
                    user = JiraUser(
                        username=f"{profile['email_prefix'].lower()}",
                        full_name=f"{profile['first_name']} {profile['last_name']}",
                        email=f"{profile['email_prefix'].lower()}@mahalopay.com",
                        role=profile['role']
                    )
                    db.add(user)
                    users.append(user)
                
                db.commit()
                db.refresh(users[-1])  # ensure IDs are available
                users = db.query(JiraUser).all()
                result["users"] = users_needed - len(existing_users)
                print(f"  Committed {result['users']} users to DB.")

        # Generate JIRA stories
        if jira_stories > 0:
            print(f"Generating {jira_stories} JIRA stories with LLM...")
            existing_story_keys = [s.story_key for s in db.query(JiraStory.story_key).all()]

            # Batch stories in groups of 10
            STORY_BATCH = 10
            remaining = jira_stories
            batch_num = 0

            # Create sprints if needed
            sprint_names = []
            if jira_sprints > 0:
                existing_sprint_names = [s.sprint_name for s in db.query(JiraSprint.sprint_name).all()]
                sprint_start = len(existing_sprint_names) + 1
                
                for i in range(jira_sprints):
                    sprint = JiraSprint(
                        sprint_name=f"Sprint {sprint_start + i}",
                        goal=f"Deliver payment platform improvements",
                        velocity=random.choice([21, 26, 34, 42]),
                        completed_stories=0,
                        total_stories=0,
                        status=random.choice(["Planned", "Active", "Completed"]),
                    )
                    db.add(sprint)
                    sprint_names.append(sprint.sprint_name)
                    result["jira_sprints"] += 1
                db.commit()
                print(f"  Committed {result['jira_sprints']} sprints to DB.")
            
            story_counter = len(existing_story_keys) + 1
            
            while remaining > 0:
                batch = min(STORY_BATCH, remaining)
                batch_num += 1
                print(f"  Batch {batch_num}: generating {batch} stories ({jira_stories - remaining + batch}/{jira_stories})...")
                try:
                    batch_data = await generator.generate_jira_stories(batch, existing_story_keys, users)
                except (httpx.ReadTimeout, httpx.ConnectTimeout):
                    print(f"    Timeout, skipping batch.")
                    remaining -= batch
                    continue

                for story_info in batch_data:
                    story = JiraStory(
                        story_key=f"PAY-{story_counter:04d}",
                        title=story_info["title"][:200],
                        description=story_info["description"],
                        assignee_id=random.choice(users).id,
                        reporter_id=random.choice(users).id,
                        story_points=story_info["story_points"],
                        priority=story_info["priority"],
                        sprint=random.choice(sprint_names) if sprint_names else "Backlog",
                        status=story_info["status"],
                    )
                    db.add(story)
                    story_counter += 1
                    result["jira_stories"] += 1

                db.commit()
                print(f"    Committed {len(batch_data)} stories to DB (total: {result['jira_stories']}).")
                remaining -= batch

        # Generate JIRA bugs
        if jira_bugs > 0:
            print(f"Generating {jira_bugs} JIRA bugs with LLM...")
            existing_bug_keys = [b.bug_key for b in db.query(JiraBug.bug_key).all()]
            all_stories = db.query(JiraStory).all()

            try:
                bug_data = await generator.generate_jira_bugs(jira_bugs, existing_bug_keys, all_stories, users)
            except (httpx.ReadTimeout, httpx.ConnectTimeout):
                print("    Timeout generating bugs, skipping.")
                bug_data = []

            bug_counter = len(existing_bug_keys) + 1

            for bug_info in bug_data:
                related_story = random.choice(all_stories) if all_stories and random.random() > 0.5 else None
                
                bug = JiraBug(
                    bug_key=f"BUG-{bug_counter:04d}",
                    title=bug_info["title"][:200],
                    description=bug_info["description"],
                    assignee_id=random.choice(users).id,
                    reporter_id=random.choice(users).id,
                    severity=bug_info["severity"],
                    status=bug_info["status"],
                    related_story_id=related_story.id if related_story else None,
                )
                db.add(bug)
                bug_counter += 1
                result["jira_bugs"] += 1

            if bug_data:
                db.commit()
                print(f"  Committed {result['jira_bugs']} bugs to DB.")

        # Generate ServiceNow incidents
        if servicenow_incidents > 0:
            print(f"Generating {servicenow_incidents} ServiceNow incidents with LLM...")
            existing_incident_keys = [i.incident_id for i in db.query(ServiceNowIncident).all()]

            INCIDENT_BATCH = 10
            incident_counter = len(existing_incident_keys) + 1
            remaining = servicenow_incidents
            batch_num = 0
            while remaining > 0:
                batch = min(INCIDENT_BATCH, remaining)
                batch_num += 1
                print(f"  Batch {batch_num}: generating {batch} incidents ({servicenow_incidents - remaining + batch}/{servicenow_incidents})...")
                try:
                    batch_data = await generator.generate_servicenow_incidents(batch, existing_incident_keys)
                except (httpx.ReadTimeout, httpx.ConnectTimeout):
                        print(f"    Timeout, skipping batch.")
                        remaining -= batch
                        continue

                for incident_info in batch_data:
                    incident = ServiceNowIncident(
                        incident_id=f"INC{incident_counter:06d}",
                        title=incident_info["title"][:200],
                        description=incident_info["description"],
                        severity=incident_info["severity"],
                        status=incident_info["status"],
                        assigned_group=incident_info["assigned_group"],
                    )
                    db.add(incident)
                    incident_counter += 1
                    result["servicenow_incidents"] += 1

                db.commit()
                print(f"    Committed {len(batch_data)} incidents to DB (total: {result['servicenow_incidents']}).")
                remaining -= batch

        # Generate ServiceNow deployments
        if servicenow_deployments > 0:
            print(f"Generating {servicenow_deployments} ServiceNow deployments with LLM...")
            existing_deployment_keys = [d.deployment_id for d in db.query(ServiceNowDeployment).all()]

            try:
                deployment_data = await generator.generate_deployments(servicenow_deployments, existing_deployment_keys)
            except (httpx.ReadTimeout, httpx.ConnectTimeout):
                print("    Timeout generating deployments, skipping.")
                deployment_data = []

            deployment_counter = len(existing_deployment_keys) + 1

            for deployment_info in deployment_data:
                deployment = ServiceNowDeployment(
                    deployment_id=f"DEPLOY{deployment_counter:06d}",
                    feature_name=deployment_info["feature_name"][:200],
                    version=deployment_info["version"],
                    environment=deployment_info["environment"],
                    status=deployment_info["status"],
                    deployed_by=deployment_info["deployed_by"],
                )
                db.add(deployment)
                deployment_counter += 1
                result["servicenow_deployments"] += 1

            if deployment_data:
                db.commit()

                print(f"  Committed {result['servicenow_deployments']} deployments to DB.")

        # Generate Splunk logs
        if splunk_logs > 0:
            print(f"Generating {splunk_logs} Splunk logs with LLM...")

            BATCH_SIZE = 10
            now = datetime.utcnow()
            remaining = splunk_logs
            batch_num = 0
            
            while remaining > 0:
                batch = min(BATCH_SIZE, remaining)
                batch_num += 1
                print(f"  Batch {batch_num}: generating {batch} logs ({splunk_logs - remaining + batch}/{splunk_logs})...")
                for attempt in range(3):
                    try:
                        log_data = await generator.generate_splunk_logs(batch)
                        break
                    except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                        if attempt < 2:
                            print(f"    Timeout, retrying ({attempt + 2}/3)...")
                            await asyncio.sleep(2)
                        else:
                            print(f"    Skipping batch after 3 timeouts.")
                            log_data = []

                for log_info in log_data:
                    log = SplunkLog(
                        source=log_info["source"],
                        level=log_info["level"],
                        message=log_info["message"],
                        service=log_info["service"],
                        timestamp=now - timedelta(minutes=random.randint(0, 60 * 24 * 30)),
                    )
                    db.add(log)
                    result["splunk_logs"] += 1

                if log_data:
                    db.commit()
                    print(f"    Committed {len(log_data)} logs to DB (total: {result['splunk_logs']}).")
                remaining -= batch

        return result
        
    except Exception as e:
        db.rollback()
        print(f"Error generating test data: {e}")
        raise
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate realistic test data using LLM for better variety and context."
    )
    
    # New argument format
    parser.add_argument("--jira-stories", type=int, default=0, help="Number of JIRA stories to generate")
    parser.add_argument("--jira-bugs", type=int, default=0, help="Number of JIRA bugs to generate")
    parser.add_argument("--jira-sprints", type=int, default=0, help="Number of JIRA sprints to generate")
    parser.add_argument("--servicenow-incidents", type=int, default=0, help="Number of ServiceNow incidents")
    parser.add_argument("--servicenow-deployments", type=int, default=0, help="Number of ServiceNow deployments")
    parser.add_argument("--splunk-logs", type=int, default=0, help="Number of Splunk logs")
    
    # Legacy argument format for backward compatibility
    parser.add_argument("--jira-data", type=int, default=0, help="(Legacy) Generate N JIRA stories + bugs + sprints")
    parser.add_argument("--servicenow-data", type=int, default=0, help="(Legacy) Generate N ServiceNow incidents")
    parser.add_argument("--splunk-data", type=int, default=0, help="(Legacy) Generate N Splunk logs")
    
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--reset", action="store_true", help="Reset database before generating")
    parser.add_argument("--quick", action="store_true", help="Generate a quick demo dataset (10 of each)")
    
    args = parser.parse_args()
    
    # Handle quick mode
    if args.quick:
        args.jira_stories = 25
        args.jira_bugs = 10
        args.jira_sprints = 4
        args.servicenow_incidents = 30
        args.servicenow_deployments = 15
        args.splunk_logs = 200
    # Handle legacy arguments
    elif args.jira_data > 0 or args.servicenow_data > 0 or args.splunk_data > 0:
        if args.jira_data > 0:
            args.jira_stories = args.jira_data
            args.jira_bugs = max(1, args.jira_data // 5)
            args.jira_sprints = max(1, args.jira_data // 10)
        if args.servicenow_data > 0:
            args.servicenow_incidents = args.servicenow_data
        if args.splunk_data > 0:
            args.splunk_logs = args.splunk_data
    
    result = asyncio.run(generate_enhanced_test_data(
        jira_stories=args.jira_stories,
        jira_bugs=args.jira_bugs,
        jira_sprints=args.jira_sprints,
        servicenow_incidents=args.servicenow_incidents,
        servicenow_deployments=args.servicenow_deployments,
        splunk_logs=args.splunk_logs,
        seed=args.seed,
        reset=args.reset,
    ))
    
    print("\n" + "="*60)
    print("✅ Enhanced Test Data Generation Complete!")
    print("="*60)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
