"""
Diagnostic script to check LLM test data generator configuration.
Run this before generating test data to verify everything is set up correctly.
"""
import os
import sys
from pathlib import Path

# Change to script directory and add to path
script_dir = Path(__file__).parent.parent.parent
os.chdir(script_dir)
sys.path.insert(0, str(script_dir))

try:
    from backend.config import settings
except ImportError:
    print("Error: Could not import backend.config")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    sys.exit(1)


def check_configuration():
    """Check if LLM test data generator is properly configured."""
    print("="*70)
    print("🔍 LLM Test Data Generator - Configuration Check")
    print("="*70)
    print()
    
    issues = []
    warnings = []
    
    # Check 1: API Key
    print("1. Checking API Key...")
    if settings.ONE_MIN_AI_API_KEY and len(settings.ONE_MIN_AI_API_KEY) > 10:
        print(f"   ✅ API key found: {settings.ONE_MIN_AI_API_KEY[:10]}...{settings.ONE_MIN_AI_API_KEY[-4:]}")
    else:
        print(f"   ❌ API key not configured or invalid")
        issues.append("API key not set in .env file")
        print("      Set ONE_MIN_AI_API_KEY in your .env file")
    print()
    
    # Check 2: Base URL
    print("2. Checking Base URL...")
    print(f"   ℹ️  Base URL: {settings.ONE_MIN_AI_BASE_URL}")
    print()
    
    # Check 3: Model
    print("3. Checking Model...")
    print(f"   ℹ️  Model: {settings.LITELLM_MODEL}")
    print()
    
    # Check 4: Database
    print("4. Checking Database...")
    print(f"   ℹ️  Database URL: {settings.DATABASE_URL}")
    if "sqlite" in settings.DATABASE_URL:
        db_path = settings.DATABASE_URL.replace("sqlite:///", "").replace("./", "")
        if os.path.exists(db_path):
            print(f"   ✅ Database file exists: {db_path}")
        else:
            print(f"   ⚠️  Database file will be created: {db_path}")
            warnings.append("Database doesn't exist yet (will be created)")
    print()
    
    # Check 5: Import test
    print("5. Checking Python dependencies...")
    try:
        import openai
        print(f"   ✅ openai package installed: v{openai.__version__}")
    except ImportError:
        print("   ❌ openai package not installed")
        issues.append("Run: pip install openai")
    
    try:
        import httpx
        print(f"   ✅ httpx package installed: v{httpx.__version__}")
    except ImportError:
        print("   ❌ httpx package not installed")
        issues.append("Run: pip install httpx")
    
    try:
        import sqlalchemy
        print(f"   ✅ sqlalchemy package installed: v{sqlalchemy.__version__}")
    except ImportError:
        print("   ❌ sqlalchemy package not installed")
        issues.append("Run: pip install sqlalchemy")
    print()
    
    # Check 6: Test API connection
    print("6. Testing API Connection...")
    if settings.ONE_MIN_AI_API_KEY and len(settings.ONE_MIN_AI_API_KEY) > 10:
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=settings.ONE_MIN_AI_API_KEY,
                base_url=settings.ONE_MIN_AI_BASE_URL,
            )
            # Simple test call
            response = client.chat.completions.create(
                model=settings.LITELLM_MODEL,
                messages=[{"role": "user", "content": "Say 'test'"}],
                max_tokens=5,
            )
            print("   ✅ API connection successful!")
            print(f"      Response: {response.choices[0].message.content}")
        except Exception as e:
            print(f"   ❌ API connection failed: {str(e)}")
            issues.append(f"API connection error: {str(e)}")
    else:
        print("   ⏭️  Skipped (no API key)")
    print()
    
    # Summary
    print("="*70)
    print("📋 Summary")
    print("="*70)
    
    if not issues and not warnings:
        print("✅ All checks passed! You're ready to generate test data.")
        print()
        print("Run: python backend/utils/generate_test_data_llm.py --quick")
        print("Or:  scripts\\generate_test_data.bat")
        return 0
    
    if warnings:
        print()
        print("⚠️  Warnings:")
        for warning in warnings:
            print(f"   - {warning}")
    
    if issues:
        print()
        print("❌ Issues found:")
        for issue in issues:
            print(f"   - {issue}")
        print()
        print("Please fix these issues before running the generator.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(check_configuration())
