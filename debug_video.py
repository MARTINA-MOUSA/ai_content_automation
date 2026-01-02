from app.services.content_fetcher import extract_youtube
from app.services.ai_service import validate_ai_news
import sys
import os

# Set encoding for title display in case we want to print something
# But we'll write to a file to be safe.

url = "https://youtu.be/nzYR9BwrBMM?si=J7GypOrFbucGHEer"

with open("debug_output.txt", "w", encoding="utf-8") as f:
    f.write(f"Testing URL: {url}\n")
    try:
        data = extract_youtube(url)
        f.write("\n--- METADATA ---\n")
        f.write(str(data['metadata']) + "\n")
        
        f.write("\n--- EXTRACTED RAW TEXT (FIRST 500) ---\n")
        f.write(data['raw_text'][:500] + "\n")
        
        is_ai = validate_ai_news(data['raw_text'])
        f.write(f"\nFinal Validation Result: {is_ai}\n")
        
    except Exception as e:
        f.write(f"\nERROR: {str(e)}\n")

print("Diagnostic finished. Check debug_output.txt")
