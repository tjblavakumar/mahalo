"""
Test script to verify the fix for production features query issue.

The issue: When asking "how many features are in production already", 
the system was responding with critical incidents instead of deployment counts.

The fix: Prioritize deployment-specific queries in the fallback_response method
before correlation engine insights that may include critical incidents.
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
        
        # Also include incidents (which should NOT be shown for deployment queries)
        incidents = [
            {
                "incident_id": "INC-001",
                "title": "Payment service returning 500 errors during peak load",
                "severity": "Critical",
                "status": "Active"
            },
            {
                "incident_id": "INC-002", 
                "title": "Payment API latency spike",
                "severity": "Critical",
                "status": "Active"
            },
            {
                "incident_id": "INC-003",
                "title": "Settlement job failure",
                "severity": "Critical",
                "status": "New"
            }
        ]
        
        return {
            "source": "ServiceNow",
            "record_type": "deployments",
            "query": query,
            "success": True,
            "data": {
                "items": deployments,
                "deployments": deployments,
                "incidents": incidents
            }
        }


class MockJiraAgent:
    """Mock JIRA agent."""
    async def retrieve_context(self, query):
        return {
            "source": "JIRA",
            "success": True,
            "data": {"items": []}
        }


class MockSplunkAgent:
    """Mock Splunk agent."""
    async def retrieve_context(self, query):
        return {
            "source": "Splunk",
            "success": True,
            "data": {"items": []}
        }


async def test_production_features_query():
    """Test that 'how many features in production' returns deployment count, not incidents."""
    
    # Create orchestrator with mocked agents
    orchestrator = OrchestratorAgent(
        jira_agent=MockJiraAgent(),
        servicenow_agent=MockServiceNowAgent(),
        splunk_agent=MockSplunkAgent()
    )
    
    # Test the query
    query = "how many features are in production already"
    response = await orchestrator.process_query("Executive", query)
    
    print("=" * 70)
    print(f"Query: {query}")
    print("=" * 70)
    print(f"Response:\n{response}")
    print("=" * 70)
    
    # Verify the response
    assert "5 features are deployed in production" in response, \
        f"Expected deployment count, got: {response}"
    
    assert "Stripe payment gateway integration" in response, \
        f"Expected feature names in response, got: {response}"
    
    # Make sure incidents are NOT mentioned
    assert "INC-001" not in response, \
        f"Response should not contain incident IDs, got: {response}"
    
    assert "500 errors" not in response, \
        f"Response should not contain incident details, got: {response}"
    
    assert "Critical" not in response or "Critical Incident" not in response, \
        f"Response should focus on deployments, not incidents, got: {response}"
    
    print("\n✅ TEST PASSED: Production features query returns deployment count, not incidents!")
    print("\nThe fix successfully prioritizes deployment data over correlation engine")
    print("insights that may include critical incidents.")
    
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(test_production_features_query())
        if result:
            print("\n" + "=" * 70)
            print("SUCCESS: The fix resolves the reported issue!")
            print("=" * 70)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
