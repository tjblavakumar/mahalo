"""Test script to debug agent data retrieval"""
import asyncio
from agents.orchestrator import OrchestratorAgent


async def test_agents():
    orchestrator = OrchestratorAgent()
    
    print("Testing orchestrator with executive query...")
    print("=" * 60)
    
    response = await orchestrator.process_query(
        user_persona="Executive",
        user_query="executive summary",
        conversation_history=[]
    )
    
    print(f"\nResponse: {response}")
    print(f"\nAgents used: {orchestrator.last_agents_used}")
    print(f"\nContexts retrieved:")
    for context in orchestrator.last_contexts:
        print(f"  - Source: {context.get('source')}")
        print(f"    Success: {context.get('success')}")
        print(f"    Data items: {len(context.get('data', {}).get('items', []))}")
        if not context.get('success'):
            print(f"    Error: {context.get('error')}")
        print()


if __name__ == "__main__":
    asyncio.run(test_agents())
