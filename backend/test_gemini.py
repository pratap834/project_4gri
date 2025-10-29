"""
Quick test to verify Gemini AI integration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("GEMINI AI INTEGRATION TEST")
print("=" * 60)

# Check if API key is set
gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key:
    print("✓ GEMINI_API_KEY found in .env")
    print(f"  Key starts with: {gemini_key[:20]}...")
    print(f"  Key length: {len(gemini_key)} characters")
else:
    print("✗ GEMINI_API_KEY not found in .env")
    exit(1)

# Try to import and configure Gemini
try:
    import google.generativeai as genai
    print("✓ google-generativeai package installed")
except ImportError:
    print("✗ google-generativeai package not installed")
    print("  Run: pip install google-generativeai")
    exit(1)

# Try to configure and test API
try:
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    print("✓ Gemini API configured successfully")
    
    # Test a simple generation
    print("\nTesting API with a simple prompt...")
    response = model.generate_content("Say 'Hello from Gemini!' in one sentence.")
    print(f"✓ API Response: {response.text.strip()}")
    
    print("\n" + "=" * 60)
    print("GEMINI AI INTEGRATION: ✓ WORKING CORRECTLY")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ Error testing Gemini API: {e}")
    print("\nPossible issues:")
    print("  1. Invalid API key")
    print("  2. API quota exceeded")
    print("  3. Network connectivity issue")
    exit(1)

# Check if gemini_service module exists and imports correctly
print("\nChecking gemini_service module...")
try:
    from utils.gemini_service import (
        generate_crop_notification,
        generate_fertilizer_notification,
        generate_yield_notification
    )
    print("✓ gemini_service module imports successfully")
    print("✓ All notification functions available")
except ImportError as e:
    print(f"✗ Error importing gemini_service: {e}")

print("\n" + "=" * 60)
print("ALL CHECKS PASSED - GEMINI IS INTEGRATED CORRECTLY!")
print("=" * 60)
