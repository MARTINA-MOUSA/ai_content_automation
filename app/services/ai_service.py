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
        return True # Default to True if client is missing to avoid blocking users
        
    text_content = text.lower()
    
    # Keyword-based fallback (Safety Net)
    ai_keywords = [
        "ai", "artificial intelligence", "machine learning", "llm", "gpt", 
        "openai", "gemini", "claude", "deepseek", "neural", "robotics",
        "automation", "nvidia", "transformer", "diffusion", "rag"
    ]
    
    # Check if any keyword exists in the text (Title, Description, or Transcript)
    if any(kw in text_content for kw in ai_keywords):
        print(f">>> [Validation] Found AI keyword in content. Bypassing LLM check.")
        return True

    # If the text is extremely short or default failure text, don't block.
    if len(text.strip()) < 100 or "Transcript not available" in text:
        return True
        
    try:
        prompt = f"""
        Is the following content related to Artificial Intelligence (AI), Machine Learning, LLMs, or AI-related technology news?
        
        Answer YES or NO.
        
        Content:
        {text[:5000]}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0
            )
        )
        
        if hasattr(response, 'text') and response.text:
            answer = response.text.strip().upper()
            if "NO" in answer and "YES" not in answer:
                # One last check: If the URL itself has "ai", we still pass
                return False
            return True
        return True
            
    except Exception as e:
        print(f"Validation Error: {e}")
        return True

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
