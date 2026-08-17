"""
Compare the output of original vs LLM-enhanced test data generators.
This script shows side-by-side comparison of generated data quality.
"""
import asyncio
import json

from backend.database import SessionLocal, init_db
from backend.models.jira_models import JiraStory, JiraBug
from backend.models.servicenow_models import ServiceNowIncident
from backend.utils.generate_test_data import generate_test_data
from backend.utils.generate_test_data_llm import generate_enhanced_test_data


async def show_comparison():
    """Generate sample data from both generators and compare."""
    
    print("="*80)
    print("TEST DATA GENERATOR COMPARISON")
    print("="*80)
    print()
    
    # Generate with original generator
    print("📊 Generating with ORIGINAL generator...")
    result_original = generate_test_data(
        jira_data=3,
        servicenow_data=2,
        seed=42,
        reset=True
    )
    print(f"✓ Generated: {result_original}")
    print()
    
    # Query original data
    db = SessionLocal()
    original_stories = db.query(JiraStory).limit(3).all()
    original_bugs = db.query(JiraBug).limit(2).all()
    original_incidents = db.query(ServiceNowIncident).limit(2).all()
    db.close()
    
    print("\n" + "="*80)
    print("ORIGINAL GENERATOR OUTPUT")
    print("="*80)
    
    for i, story in enumerate(original_stories, 1):
        print(f"\n📝 Story {i}:")
        print(f"  Key: {story.story_key}")
        print(f"  Title: {story.title}")
        print(f"  Description: {story.description[:100]}...")
        print(f"  Length: {len(story.description)} chars")
    
    for i, bug in enumerate(original_bugs, 1):
        print(f"\n🐛 Bug {i}:")
        print(f"  Key: {bug.bug_key}")
        print(f"  Title: {bug.title}")
        print(f"  Description: {bug.description[:100]}...")
        print(f"  Length: {len(bug.description)} chars")
    
    for i, incident in enumerate(original_incidents, 1):
        print(f"\n🚨 Incident {i}:")
        print(f"  ID: {incident.incident_id}")
        print(f"  Title: {incident.title}")
        print(f"  Description: {incident.description[:100]}...")
        print(f"  Length: {len(incident.description)} chars")
    
    # Generate with LLM generator
    print("\n\n" + "="*80)
    print("🤖 Generating with LLM-ENHANCED generator...")
    print("="*80)
    
    result_llm = await generate_enhanced_test_data(
        jira_stories=3,
        jira_bugs=2,
        servicenow_incidents=2,
        seed=43,
        reset=True
    )
    print(f"✓ Generated: {result_llm}")
    
    # Query LLM data
    db = SessionLocal()
    llm_stories = db.query(JiraStory).limit(3).all()
    llm_bugs = db.query(JiraBug).limit(2).all()
    llm_incidents = db.query(ServiceNowIncident).limit(2).all()
    db.close()
    
    print("\n" + "="*80)
    print("LLM-ENHANCED GENERATOR OUTPUT")
    print("="*80)
    
    for i, story in enumerate(llm_stories, 1):
        print(f"\n📝 Story {i}:")
        print(f"  Key: {story.story_key}")
        print(f"  Title: {story.title}")
        print(f"  Description Preview:")
        # Show first 300 chars with proper wrapping
        desc_lines = story.description[:400].split('\n')
        for line in desc_lines[:5]:
            print(f"    {line}")
        if len(story.description) > 400:
            print(f"    ... (total {len(story.description)} chars)")
    
    for i, bug in enumerate(llm_bugs, 1):
        print(f"\n🐛 Bug {i}:")
        print(f"  Key: {bug.bug_key}")
        print(f"  Title: {bug.title}")
        print(f"  Description Preview:")
        desc_lines = bug.description[:400].split('\n')
        for line in desc_lines[:5]:
            print(f"    {line}")
        if len(bug.description) > 400:
            print(f"    ... (total {len(bug.description)} chars)")
    
    for i, incident in enumerate(llm_incidents, 1):
        print(f"\n🚨 Incident {i}:")
        print(f"  ID: {incident.incident_id}")
        print(f"  Title: {incident.title}")
        print(f"  Description Preview:")
        desc_lines = incident.description[:400].split('\n')
        for line in desc_lines[:5]:
            print(f"    {line}")
        if len(incident.description) > 400:
            print(f"    ... (total {len(incident.description)} chars)")
    
    # Statistics
    print("\n\n" + "="*80)
    print("📊 COMPARISON STATISTICS")
    print("="*80)
    
    orig_story_lengths = [len(s.description or "") for s in original_stories]
    llm_story_lengths = [len(s.description or "") for s in llm_stories]
    
    orig_bug_lengths = [len(b.description or "") for b in original_bugs]
    llm_bug_lengths = [len(b.description or "") for b in llm_bugs]
    
    orig_incident_lengths = [len(i.description or "") for i in original_incidents]
    llm_incident_lengths = [len(i.description or "") for i in llm_incidents]
    
    print(f"\n📝 Story Descriptions:")
    print(f"  Original: Avg {sum(orig_story_lengths)/len(orig_story_lengths):.0f} chars")
    print(f"  LLM:      Avg {sum(llm_story_lengths)/len(llm_story_lengths):.0f} chars")
    print(f"  Improvement: {(sum(llm_story_lengths)/sum(orig_story_lengths) - 1) * 100:.0f}% more detailed")
    
    print(f"\n🐛 Bug Descriptions:")
    print(f"  Original: Avg {sum(orig_bug_lengths)/len(orig_bug_lengths):.0f} chars")
    print(f"  LLM:      Avg {sum(llm_bug_lengths)/len(llm_bug_lengths):.0f} chars")
    print(f"  Improvement: {(sum(llm_bug_lengths)/sum(orig_bug_lengths) - 1) * 100:.0f}% more detailed")
    
    print(f"\n🚨 Incident Descriptions:")
    print(f"  Original: Avg {sum(orig_incident_lengths)/len(orig_incident_lengths):.0f} chars")
    print(f"  LLM:      Avg {sum(llm_incident_lengths)/len(llm_incident_lengths):.0f} chars")
    print(f"  Improvement: {(sum(llm_incident_lengths)/sum(orig_incident_lengths) - 1) * 100:.0f}% more detailed")
    
    print("\n" + "="*80)
    print("✨ KEY DIFFERENCES")
    print("="*80)
    print("""
Original Generator:
  ✓ Fast and deterministic
  ✓ Good for CI/CD pipelines
  ✗ Generic descriptions
  ✗ Repetitive patterns
  ✗ Limited context

LLM-Enhanced Generator:
  ✓ Realistic and diverse
  ✓ Rich technical context
  ✓ Unique descriptions
  ✓ Acceptance criteria included
  ✓ Business value explained
  ✗ Requires API calls
  ✗ Slightly slower

Recommendation:
  - Use ORIGINAL for: Fast local testing, CI/CD
  - Use LLM-ENHANCED for: Demos, realistic testing, development
""")
    
    print("="*80)


if __name__ == "__main__":
    asyncio.run(show_comparison())
