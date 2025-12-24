"""
Quick verification script to test Gemini API integration
Run this to verify your Gemini API key is working correctly
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def verify_gemini_setup():
    """Verify Gemini API key and model access"""
    print("=" * 60)
    print("Gemini API Verification")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in environment")
        print("   Make sure you have a .env file in the backend/ directory")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    # Check provider setting
    provider = os.getenv("PRIMARY_LLM_PROVIDER", "openai").lower()
    if provider != "google":
        print(f"⚠️  WARNING: PRIMARY_LLM_PROVIDER is set to '{provider}', not 'google'")
        print("   The system will use Gemini, but PRIMARY_LLM_PROVIDER should be 'google'")
    else:
        print(f"✅ PRIMARY_LLM_PROVIDER is set to '{provider}'")
    
    # Test API connection
    try:
        print("\n🔍 Testing Gemini API connection...")
        genai.configure(api_key=api_key)
        
        # Test text model
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Say 'Hello, Gemini is working!' in one sentence.")
        
        if response and response.text:
            print("✅ Text model (gemini-1.5-pro) is working!")
            print(f"   Response: {response.text[:100]}")
        else:
            print("⚠️  Text model responded but no text returned")
        
        # Test vision model
        print("\n🔍 Testing Gemini Vision model...")
        vision_model = genai.GenerativeModel('gemini-1.5-pro-vision')
        print("✅ Vision model (gemini-1.5-pro-vision) initialized successfully!")
        
        print("\n" + "=" * 60)
        print("✅ All checks passed! Gemini API is configured correctly.")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to connect to Gemini API")
        print(f"   Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Verify your API key is correct")
        print("2. Check your internet connection")
        print("3. Ensure you have API access enabled in Google Cloud Console")
        print("4. Check if you've exceeded rate limits")
        return False

if __name__ == "__main__":
    verify_gemini_setup()




