import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import openai

def test_models():
    load_dotenv()
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
    
    print("Testing API keys:")
    print(f"Gemini API Key: {'Found' if gemini_api_key else 'Not found'}")
    print(f"OpenRouter API Key: {'Found' if openrouter_api_key else 'Not found'}")
    
    # Test Gemini
    if gemini_api_key:
        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-001')
            response = model.generate_content("Say hello world")
            print("Gemini test successful:", response.text[:50])
        except Exception as e:
            print("Gemini test failed:", str(e))
    
    # Test OpenRouter
    if openrouter_api_key:
        try:
            client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=openrouter_api_key,
            )
            response = client.chat.completions.create(
                model="kwaipilot/kat-coder-pro:free",
                messages=[{"role": "user", "content": "Say hello world"}],
                temperature=0.7,
                max_tokens=100,
            )
            print("OpenRouter test successful:", response.choices[0].message.content[:50])
        except Exception as e:
            print("OpenRouter test failed:", str(e))

if __name__ == "__main__":
    test_models()