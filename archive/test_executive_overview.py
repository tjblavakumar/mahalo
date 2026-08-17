"""Test orchestrator executive overview queries"""
import asyncio
from agents.orchestrator import OrchestratorAgent


async def test_executive_queries():
    orchestrator = OrchestratorAgent()
    
    test_queries = [
        "give me the elaborated overview of the project",
        "give me the elaborated executive summary of the project",
        "give me executive overview",
        "executive summary",
        "project overview",
        "summary of the project",
    ]
    
    print("=" * 80)
    print("TESTING ORCHESTRATOR EXECUTIVE OVERVIEW QUERIES")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\n>> Testing: '{query}'")
        print("-" * 80)
        
        result = await orchestrator.process_query("Executive", query, None)
        
        # Check if it's returning story draft (BAD) or executive summary (GOOD)
        is_story_draft = "JIRA story draft" in result or "acceptance criteria" in result
        is_executive_summary = "executive update" in result or "SUMMARY:" in result or "HEALTH SCORE:" in result
        
        if is_story_draft:
            print("[FAIL] Returned story draft instead of executive summary")
            print(f"   Response preview: {result[:200]}...")
        elif is_executive_summary:
            print("[PASS] Returned executive summary")
            # Show first few lines
            lines = result.split('\n')[:10]
            for line in lines:
                print(f"   {line}")
            if len(result.split('\n')) > 10:
                print("   ...")
        else:
            print("[UNKNOWN] Response doesn't match expected patterns")
            print(f"   Response preview: {result[:200]}...")


if __name__ == "__main__":
    asyncio.run(test_executive_queries())
