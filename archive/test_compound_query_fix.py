"""
Test script to verify the fix for compound production + priority query.

The issue: When asking "what is in production now and what is high priority next",
the system was showing raw data with "unknown" values instead of a proper formatted response.

The fix: Expand compound query detection to include "priority"/"next" keywords,
and ensure proper data extraction from ServiceNow response.
"""
import asyncio
from agents.orchestrator import OrchestratorAgent


class MockServiceNowAgent:
    """Mock ServiceNow agent that returns deployment data."""
    
    async def retrieve_context(self, query):
        # Simulate deployments in production
        deployments = [
            {"feature_name": "Stripe payment gateway integration", "version": "v2.4.0"},
            {"feature_name": "Fraud detection rules engine", "version": "v1.8.2"},
            {"feature_name": "ACH payment processor", "version": "v3.1.0"},
            {"feature_name": "Multi-currency support", "version": "v1.5.0"},
            {"feature_name": "Payment reconciliation dashboard", "version": "v2.0.1"},
        ]
        
        return {
            "source": "ServiceNow",
            "record_type": "deployments",
            "query": query,
            "success": True,
            "data": {
                "items": deployments
            }
        }


class MockJiraAgent:
    """Mock JIRA agent that returns backlog stories."""
    async def retrieve_context(self, query):
        # Simulate pending stories
        stories = [
            {
                "story_key": "STORY-201",
                "title": "Implement payment gateway failover",
                "status": "Backlog",
                "priority": "High",
                "story_points": 8
            },
            {
                "story_key": "STORY-202",
                "title": "Add fraud detection caching layer",
                "status": "Backlog",
                "priority": "High",
                "story_points": 5
            },
            {
                "story_key": "STORY-203",
                "title": "Improve reconciliation dashboard",
                "status": "Backlog",
                "priority": "Medium",
                "story_points": 3
            }
        ]
        
        return {
            "source": "JIRA",
            "success": True,
            "data": {"items": stories}
        }


class MockSplunkAgent:
    """Mock Splunk agent."""
    async def retrieve_context(self, query):
        return {
            "source": "Splunk",
            "success": True,
            "data": {"items": []}
        }


async def test_compound_production_priority_query():
    """Test that 'what is in production now and what is high priority next' returns proper response."""
    
    # Create orchestrator with mocked agents
    orchestrator = OrchestratorAgent(
        jira_agent=MockJiraAgent(),
        servicenow_agent=MockServiceNowAgent(),
        splunk_agent=MockSplunkAgent()
    )
    
    # Test the query
    query = "what is in production now and what is high priority next"
    response = await orchestrator.process_query("Executive", query)
    
    print("=" * 70)
    print(f"Query: {query}")
    print("=" * 70)
    print(f"Response:\n{response}")
    print("=" * 70)
    
    # Verify the response is properly formatted
    assert "## In Production" in response, \
        f"Expected production section header, got: {response}"
    
    assert "## Pending in Backlog" in response or "High Priority" in response, \
        f"Expected pending/priority section, got: {response}"
    
    # Check for deployment data
    assert "Stripe payment gateway integration" in response, \
        f"Expected feature names in response, got: {response}"
    
    assert "v2.4.0" in response or "2.4.0" in response, \
        f"Expected version info in response, got: {response}"
    
    # Check for high-priority stories
    assert "STORY-201" in response or "payment gateway failover" in response.lower(), \
        f"Expected high-priority story in response, got: {response}"
    
    # Make sure it's NOT showing raw "unknown" values
    assert "unknown" not in response.lower(), \
        f"Response should not contain 'unknown' values, got: {response}"
    
    # Make sure it's NOT just listing "JIRA found X stories"
    assert not response.startswith("Executive, here is what I found"), \
        f"Response should be formatted, not raw data listing, got: {response}"
    
    print("\n✅ TEST PASSED: Compound query returns properly formatted response!")
    print("\nThe fix successfully handles compound production + priority queries")
    print("and formats them with both deployment and pending story information.")
    
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(test_compound_production_priority_query())
        if result:
            print("\n" + "=" * 70)
            print("SUCCESS: The compound query fix works correctly!")
            print("=" * 70)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
