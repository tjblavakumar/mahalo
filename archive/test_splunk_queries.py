"""Test Splunk agent query handling"""
import asyncio
from agents.splunk_agent import SplunkAgent


async def test_error_queries():
    agent = SplunkAgent()
    
    test_queries = [
        "give me the summary of logs based on errors",
        "show me errors",
        "summary of error logs",
        "all errors",
        "error summary",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        result = await agent.retrieve_context(query)
        
        print(f"Success: {result.get('success')}")
        print(f"Items returned: {len(result.get('data', {}).get('items', []))}")
        print(f"Record type: {result.get('record_type', 'N/A')}")
        
        if result.get('summary'):
            print(f"Summary: {result.get('summary')}")
        
        if result.get('data', {}).get('items'):
            items = result['data']['items']
            error_count = sum(1 for item in items if item.get('level', '').upper() == 'ERROR')
            print(f"Error logs: {error_count} / {len(items)}")
            
            # Show first 3 error messages
            errors = [item for item in items if item.get('level', '').upper() == 'ERROR']
            if errors:
                print("\nFirst 3 error messages:")
                for i, error in enumerate(errors[:3], 1):
                    print(f"  {i}. {error.get('message', 'No message')[:80]}")


if __name__ == "__main__":
    asyncio.run(test_error_queries())
