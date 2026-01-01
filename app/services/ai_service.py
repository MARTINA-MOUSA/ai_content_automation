import os
import json
from google import genai
from google.genai import types
from app.core.config import GEMINI_API_KEY

# Initialize Client
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

def validate_ai_news(text: str) -> bool:
    """Validates if the content is related to AI news or general AI topics using the new SDK."""
    if not client:
        return False
        
    try:
        prompt = f"""
        Analyze the following content (Title, Description, and/or Transcript).
        Is this content related to Artificial Intelligence (AI), Machine Learning, LLMs, or AI-related news?
        
        Answer with 'YES' if it is related, or 'NO' if it is not.
        Only respond with the word YES or NO.
        
        Content:
        {text[:8000]}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        answer = response.text.strip().upper()
        return "YES" in answer
    except Exception as e:
        print(f"Validation Error: {e}")
        return True # Default to True to avoid skipping on API errors

def analyze_content_structured(text: str) -> dict:
    """Analyzes content and returns strict JSON output using the new SDK."""
    if not client:
        return {
            "title": "Error",
            "summary": "No API Key provided.",
            "key_topics": [],
            "sentiment": "neutral"
        }

    try:
        prompt = """
        Analyze the following content and return a STRICT JSON response with these exact fields:
        {
          "title": "A catchy title for the content",
          "summary": "A concise summary (max 150 words)",
          "key_topics": ["topic1", "topic2", ...],
          "sentiment": "positive | neutral | negative"
        }
        
        Content:
        """
        full_content = f"{prompt}\n{text[:15000]}"
        
        # Use config to enforce JSON response if the model supports it, 
        # or stick to the current cleanup logic for maximum compatibility.
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_content,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"Analysis Error: {e}")
        return {
            "title": "Analysis Failed",
            "summary": f"Could not analyze content: {str(e)}",
            "key_topics": [],
            "sentiment": "neutral"
        }

def analyze_with_gemini(text: str) -> dict:
    return analyze_content_structured(text)
