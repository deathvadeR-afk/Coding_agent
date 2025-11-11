import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
    
    print("API Keys Check:")
    print(f"Gemini API Key: {'Found' if gemini_api_key else 'Not found'}")
    print(f"OpenRouter API Key: {'Found' if openrouter_api_key else 'Not found'}")
    
    if gemini_api_key:
        print("Gemini API key is available")
    if openrouter_api_key:
        print("OpenRouter API key is available")

if __name__ == "__main__":
    main()