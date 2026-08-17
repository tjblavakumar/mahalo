"""
Test script to verify proxy configuration is working correctly.
This script helps diagnose proxy-related issues.
"""
import asyncio
import httpx
import os


def print_proxy_config():
    """Print current proxy environment variables."""
    print("=" * 60)
    print("CURRENT PROXY CONFIGURATION")
    print("=" * 60)
    
    proxy_vars = ["HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy", "NO_PROXY", "no_proxy"]
    for var in proxy_vars:
        value = os.getenv(var)
        if value:
            print(f"  {var}: {value}")
        else:
            print(f"  {var}: (not set)")
    print()


async def test_httpx_proxy():
    """Test httpx with trust_env=True (proxy enabled)."""
    print("=" * 60)
    print("TESTING HTTPX WITH PROXY SUPPORT (trust_env=True)")
    print("=" * 60)
    
    # Test localhost endpoints (should bypass proxy via NO_PROXY)
    test_urls = [
        "http://localhost:5001/api/jira/stories",
        "http://localhost:5002/api/servicenow/incidents",
        "http://localhost:5003/api/splunk/logs",
    ]
    
    for url in test_urls:
        try:
            print(f"\nTesting: {url}")
            async with httpx.AsyncClient(timeout=10.0, trust_env=True) as client:
                response = await client.get(url)
                print(f"  ✓ Status: {response.status_code}")
                data = response.json()
                item_count = len(data.get("items", [])) if isinstance(data, dict) else 0
                print(f"  ✓ Items: {item_count}")
        except httpx.ConnectError as e:
            print(f"  ✗ Connection Error: {e}")
            print(f"    (Is the service running on {url.split('/')[2]}?)")
        except httpx.ProxyError as e:
            print(f"  ✗ Proxy Error: {e}")
            print(f"    (Check proxy settings and NO_PROXY configuration)")
        except Exception as e:
            print(f"  ✗ Error: {type(e).__name__}: {e}")


async def test_httpx_no_proxy():
    """Test httpx with trust_env=False (proxy disabled) - OLD BEHAVIOR."""
    print("\n" + "=" * 60)
    print("TESTING HTTPX WITHOUT PROXY (trust_env=False) - OLD BEHAVIOR")
    print("=" * 60)
    
    test_url = "http://localhost:5001/api/jira/stories"
    try:
        print(f"\nTesting: {test_url}")
        async with httpx.AsyncClient(timeout=10.0, trust_env=False) as client:
            response = await client.get(test_url)
            print(f"  ✓ Status: {response.status_code}")
            data = response.json()
            item_count = len(data.get("items", [])) if isinstance(data, dict) else 0
            print(f"  ✓ Items: {item_count}")
    except Exception as e:
        print(f"  ✗ Error: {type(e).__name__}: {e}")


def print_recommendations():
    """Print recommendations for proxy configuration."""
    print("\n" + "=" * 60)
    print("PROXY CONFIGURATION RECOMMENDATIONS")
    print("=" * 60)
    print("""
For corporate proxy setups, ensure these environment variables are set:

1. Set proxy for external traffic:
   SET HTTP_PROXY=http://your-proxy-server:port
   SET HTTPS_PROXY=http://your-proxy-server:port

2. Bypass proxy for local services:
   SET NO_PROXY=localhost,127.0.0.1,::1

3. If your proxy requires authentication:
   SET HTTP_PROXY=http://username:password@your-proxy-server:port
   SET HTTPS_PROXY=http://username:password@your-proxy-server:port

4. For Windows PowerShell:
   $env:HTTP_PROXY="http://your-proxy-server:port"
   $env:HTTPS_PROXY="http://your-proxy-server:port"
   $env:NO_PROXY="localhost,127.0.0.1"

5. You can also add these to your .env file in the project root:
   HTTP_PROXY=http://your-proxy-server:port
   HTTPS_PROXY=http://your-proxy-server:port
   NO_PROXY=localhost,127.0.0.1

After setting environment variables, restart the application.
""")


async def main():
    """Run all tests."""
    print_proxy_config()
    await test_httpx_proxy()
    await test_httpx_no_proxy()
    print_recommendations()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
