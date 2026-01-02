import os
import json
from google import genai
from google.genai import types
from app.core.config import GEMINI_API_KEY

# Initialize Client
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

import re

def validate_ai_news(text: str) -> bool:
    """Validates if the content is related to AI news or general AI topics using the new SDK."""
    if not client:
        return True # Default to True if client is missing to avoid blocking users
        
    text_content = text.lower()
    
    # Keyword-based fallback (Safety Net)
    # Using word boundaries to avoid matching "said", "paid", etc. for "ai"
    ai_keywords = [
        "ai", "artificial intelligence", "machine learning", "ml", "llm", "gpt", 
        "openai", "gemini", "claude", "deepseek", "neural", "robotics",
        "automation", "nvidia", "transformer", "diffusion", "rag", "bot",
        "agentic", "agent", "intelligence", "computing"
    ]
    
    # If the text mentions youtube, be even more permissive
    is_youtube = "youtube" in text_content or "youtu.be" in text_content
    
    if any(re.search(rf"\b{re.escape(kw)}\b", text_content) for kw in ai_keywords):
        print(f">>> [Validation] Found AI keyword in content. Bypassing LLM check.")
        return True

    # If it's a video and contains common tech keywords, let it pass
    if is_youtube and any(kw in text_content for kw in ["tech", "how", "tutorial", "news", "update"]):
        print(f">>> [Validation] YouTube tech-related content detected. Passing.")
        return True

    # If the text is short or transcript missing, don't block
    if len(text.strip()) < 150 or "transcript not available" in text_content:
        return True
        
    try:
        # LLM check as a final pass
        prompt = f"""
        Does this content talk about Artificial Intelligence (AI), Machine Learning, or related tech? 
        Answer YES or NO.
        
        Content:
        {text[:4000]}
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
