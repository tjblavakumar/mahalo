"""
Quick diagnostic script to check if backend services are running.
This helps identify if the issue is proxy-related or service-related.
"""
import asyncio
import httpx
import sys


async def check_service(name: str, url: str) -> bool:
    """Check if a service is accessible."""
    try:
        # Use trust_env=True to respect proxy settings
        async with httpx.AsyncClient(timeout=5.0, trust_env=True) as client:
            response = await client.get(url)
            if response.status_code == 200:
                print(f"✓ {name} is running on {url}")
                data = response.json()
                if isinstance(data, dict) and "items" in data:
                    print(f"  └─ Found {len(data['items'])} items")
                return True
            else:
                print(f"✗ {name} returned status {response.status_code}")
                return False
    except httpx.ConnectError:
        print(f"✗ {name} connection failed - service may not be running")
        return False
    except httpx.ProxyError as e:
        print(f"✗ {name} proxy error: {e}")
        print(f"  └─ Check NO_PROXY includes localhost")
        return False
    except Exception as e:
        print(f"✗ {name} error: {type(e).__name__}: {e}")
        return False


async def main():
    """Check all backend services."""
    print("=" * 60)
    print("MAHALO Backend Services Health Check")
    print("=" * 60)
    print()
    
    services = [
        ("JIRA API", "http://localhost:5001/api/jira/stories"),
        ("ServiceNow API", "http://localhost:5002/api/servicenow/incidents"),
        ("Splunk API", "http://localhost:5003/api/splunk/logs"),
    ]
    
    results = []
    for name, url in services:
        success = await check_service(name, url)
        results.append(success)
        print()
    
    print("=" * 60)
    if all(results):
        print("✓ All services are running correctly!")
        print("\nIf you're still getting 0 results, the issue is likely with:")
        print("  1. Query matching (check your search terms)")
        print("  2. Data in the database (may be empty)")
    else:
        print("✗ Some services are not accessible")
        print("\nTroubleshooting steps:")
        print("  1. Start the backend services:")
        print("     python backend/jira/app.py")
        print("     python backend/servicenow/app.py")
        print("     python backend/splunk/app.py")
        print()
        print("  2. Check proxy configuration:")
        print("     Set NO_PROXY=localhost,127.0.0.1")
        print()
        print("  3. Run full proxy test:")
        print("     python test_proxy_config.py")
    print("=" * 60)
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
