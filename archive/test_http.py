"""Simple HTTP test"""
import httpx
import asyncio


async def test_api():
    print("Testing direct HTTP call to JIRA API...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            print(f"Making request to http://localhost:5001/api/jira/stories")
            response = await client.get("http://localhost:5001/api/jira/stories")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_api())
