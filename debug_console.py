import sys
import os
# Add current dir to path so we can import app
sys.path.append(os.getcwd())

from app.services.content_fetcher import fetch_content_logic
from app.services.ai_service import analyze_with_gemini

def run_debug(url):
    print(f"--- Fetching Content for {url} ---")
    text = fetch_content_logic(url)
    print(f"Content Length: {len(text)} characters")
    
    print("\n--- Analyzing with Gemini ---")
    result = analyze_with_gemini(text)
    
    print("\n--- Analysis Result ---")
    print(f"Title: {result.get('title')}")
    print(f"Author: {result.get('author')}")
    print(f"Date: {result.get('date')}")
    print("\nSummary:")
    print(result.get('summary'))
    print("\nKey Points:")
    for point in result.get('key_points', []):
        print(f"- {point}")

if __name__ == "__main__":
    test_url = "https://techcrunch.com/2025/12/29/2025-was-the-year-ai-got-a-vibe-check/"
    run_debug(test_url)
