"""Test with proxy bypass"""
import httpx
import asyncio


async def test_api():
    print("Testing with NO_PROXY...")
    
    # Test without trust_env
    try:
        async with httpx.AsyncClient(timeout=10.0, trust_env=False) as client:
            print(f"Making request to http://localhost:5001/api/jira/stories")
            response = await client.get("http://localhost:5001/api/jira/stories")
            print(f"Status: {response.status_code}")
            print(f"Response length: {len(response.text)}")
            print(f"First 200 chars: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_api())
