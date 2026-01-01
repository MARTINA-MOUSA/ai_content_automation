import os
import json
import google.generativeai as genai
from app.core.config import GEMINI_API_KEY

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def validate_ai_news(text: str) -> bool:
    """Validates if the content is related to AI news or general AI topics."""
    if not GEMINI_API_KEY:
        return False
        
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        Analyze the following content (Title, Description, and/or Transcript).
        Is this content related to Artificial Intelligence (AI), Machine Learning, LLMs, or AI-related news?
        
        Answer with 'YES' if it is related, or 'NO' if it is not.
        Only respond with the word YES or NO.
        
        Content:
        {text[:8000]}
        """
        response = model.generate_content(prompt)
        answer = response.text.strip().upper()
        return "YES" in answer
    except Exception as e:
        print(f"Validation Error: {e}")
        return True # Default to True to avoid skipping on API errors if partially confident

def analyze_content_structured(text: str) -> dict:
    """Analyzes content and returns strict JSON output."""
    if not GEMINI_API_KEY:
        return {
            "title": "Error",
            "summary": "No API Key provided.",
            "key_topics": [],
            "sentiment": "neutral"
        }

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
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
        full_prompt = f"{prompt}\n{text[:15000]}"
        response = model.generate_content(full_prompt)
        
        result_text = response.text
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0]
            
        return json.loads(result_text.strip())
    except Exception as e:
        print(f"Analysis Error: {e}")
        return {
            "title": "Analysis Failed",
            "summary": f"Could not analyze content: {str(e)}",
            "key_topics": [],
            "sentiment": "neutral"
        }

def analyze_with_gemini(text: str) -> dict:
    # Retaining for compatibility if needed elsewhere, but system uses structured version
    return analyze_content_structured(text)
