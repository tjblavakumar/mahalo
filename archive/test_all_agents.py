"""Comprehensive test for all agent query handling"""
import asyncio
from agents.jira_agent import JiraAgent
from agents.servicenow_agent import ServiceNowAgent
from agents.splunk_agent import SplunkAgent


async def test_jira_agent():
    agent = JiraAgent()
    
    test_cases = [
        # Summary/overview queries
        ("show me all stories", "Should return ALL stories"),
        ("list stories", "Should return ALL stories"),
        ("summary of stories", "Should return ALL stories"),
        ("all stories", "Should return ALL stories"),
        ("executive summary", "Should return ALL stories"),
        
        # Bug queries
        ("show me bugs", "Should return ALL bugs"),
        ("all bugs", "Should return ALL bugs"),
        ("list bugs", "Should return ALL bugs"),
        
        # Specific searches (should use keywords)
        ("stories about payment", "Should search for 'payment'"),
        ("find gateway stories", "Should search for 'gateway'"),
    ]
    
    print("=" * 80)
    print("TESTING JIRA AGENT")
    print("=" * 80)
    
    for query, expected in test_cases:
        print(f"\n>> Query: '{query}'")
        print(f"   Expected: {expected}")
        
        result = await agent.retrieve_context(query)
        
        success = result.get("success")
        items = result.get("data", {}).get("items", [])
        record_type = result.get("record_type", "stories")
        
        print(f"   -> Success: {success}")
        print(f"   -> Items: {len(items)} {record_type}")
        
        if result.get("summary"):
            summary = result["summary"]
            if "total_stories" in summary:
                print(f"   -> Summary: {summary['total_stories']} total, {summary['completed_stories']} done")
            elif "total_bugs" in summary:
                print(f"   -> Summary: {summary['total_bugs']} bugs, {summary['critical_bugs']} critical")


async def test_servicenow_agent():
    agent = ServiceNowAgent()
    
    test_cases = [
        # Overview queries (should get all data)
        ("executive summary", "Should return incidents AND deployments"),
        ("overview", "Should return incidents AND deployments"),
        ("summary", "Should return incidents AND deployments"),
        ("all incidents and deployments", "Should return incidents AND deployments"),
        
        # Incident queries
        ("show me incidents", "Should return ALL incidents"),
        ("all incidents", "Should return ALL incidents"),
        ("list incidents", "Should return ALL incidents"),
        
        # Deployment queries
        ("show deployments", "Should return deployments"),
        ("production deployments", "Should return deployments"),
        
        # Specific searches
        ("incidents about payment", "Should search for 'payment'"),
    ]
    
    print("\n" + "=" * 80)
    print("TESTING SERVICENOW AGENT")
    print("=" * 80)
    
    for query, expected in test_cases:
        print(f"\n>> Query: '{query}'")
        print(f"   Expected: {expected}")
        
        result = await agent.retrieve_context(query)
        
        success = result.get("success")
        record_type = result.get("record_type", "incidents")
        
        print(f"   -> Success: {success}")
        print(f"   -> Record type: {record_type}")
        
        if record_type == "executive_overview":
            data = result.get("data", {})
            incidents = data.get("incidents", [])
            deployments = data.get("deployments", [])
            print(f"   -> Incidents: {len(incidents)}, Deployments: {len(deployments)}")
        elif record_type == "deployments":
            items = result.get("data", {}).get("items", [])
            print(f"   -> Deployments: {len(items)}")
        else:
            items = result.get("data", {}).get("items", [])
            print(f"   -> Incidents: {len(items)}")


async def test_splunk_agent():
    agent = SplunkAgent()
    
    test_cases = [
        # Error queries (should get all errors)
        ("show me errors", "Should return ALL error logs"),
        ("summary of errors", "Should return ALL error logs"),
        ("all errors", "Should return ALL error logs"),
        ("error summary", "Should return ALL error logs"),
        ("give me the summary of logs based on errors", "Should return ALL error logs"),
        
        # Log queries (should get all logs)
        ("show all logs", "Should return ALL logs"),
        ("summary of logs", "Should return ALL logs"),
        ("all logs", "Should return ALL logs"),
        
        # Specific searches
        ("logs about timeout", "Should search for 'timeout'"),
        ("find payment errors", "Should search 'payment' + filter errors"),
    ]
    
    print("\n" + "=" * 80)
    print("TESTING SPLUNK AGENT")
    print("=" * 80)
    
    for query, expected in test_cases:
        print(f"\n>> Query: '{query}'")
        print(f"   Expected: {expected}")
        
        result = await agent.retrieve_context(query)
        
        success = result.get("success")
        items = result.get("data", {}).get("items", [])
        record_type = result.get("record_type", "N/A")
        
        print(f"   -> Success: {success}")
        print(f"   -> Items: {len(items)} logs")
        print(f"   -> Record type: {record_type}")
        
        if result.get("summary"):
            summary = result["summary"]
            if "error_count" in summary:
                print(f"   -> Errors: {summary['error_count']}")


async def main():
    print("\n" + "=" * 80)
    print("COMPREHENSIVE AGENT QUERY TESTING")
    print("=" * 80 + "\n")
    
    await test_jira_agent()
    await test_servicenow_agent()
    await test_splunk_agent()
    
    print("\n" + "=" * 80)
    print("[SUCCESS] ALL TESTS COMPLETED")
    print("=" * 80)
    print("\nReview the results above to ensure all queries return expected data.")
    print("Look for:")
    print("  - Summary queries should return ALL items (not 0)")
    print("  - 'all', 'list', 'show' queries should return ALL items")
    print("  - Specific searches should filter by keywords")


if __name__ == "__main__":
    asyncio.run(main())
