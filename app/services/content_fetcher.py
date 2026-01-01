from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from newspaper import Article
import requests
from bs4 import BeautifulSoup

def get_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed.query).get("v", [None])[0]
    raise ValueError("Invalid YouTube URL")

def extract_youtube(url: str) -> dict:
    """Extract transcript, title, and description from YouTube."""
    video_id = get_video_id(url)
    
    # Try to get Title and Description for context
    title = "Unknown Title"
    description = ""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find("meta", property="og:title")["content"] if soup.find("meta", property="og:title") else "Unknown Title"
        description = soup.find("meta", property="og:description")["content"] if soup.find("meta", property="og:description") else ""
    except Exception as e:
        print(f"YouTube Meta Scrape Error: {e}")

    # Try to get Transcript
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "ar"])
        transcript_text = " ".join(item["text"] for item in transcript_list)
    except Exception:
        transcript_text = "Transcript not available."
    
    # Combine for validation/analysis context
    raw_text = f"TITLE: {title}\n\nDESCRIPTION: {description}\n\nTRANSCRIPT: {transcript_text}"
    
    return {
        "raw_text": raw_text,
        "metadata": {
            "author": "YouTube Creator",
            "date": "Unknown",
            "source": url,
            "title": title
        }
    }

from newspaper import Article, Config

def extract_blog(url: str) -> dict:
    """Extract article text and metadata using newspaper3k with custom headers."""
    config = Config()
    config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    config.request_timeout = 10
    
    try:
        article = Article(url, config=config)
        article.download()
        article.parse()
        return {
            "raw_text": article.text,
            "metadata": {
                "author": ", ".join(article.authors) if article.authors else "Unknown",
                "date": str(article.publish_date) if article.publish_date else "Unknown",
                "source": url,
                "title": article.title
            }
        }
    except Exception as e:
        print(f"Blog Extraction Error: {e}")
        # Fallback to simple BS4
        try:
            headers = {'User-Agent': config.browser_user_agent}
            response = requests.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract only text from body to avoid scripts/nav
            body = soup.find('body')
            text = body.get_text() if body else soup.get_text()
            return {
                "raw_text": text,
                "metadata": {
                    "author": "Unknown",
                    "date": "Unknown",
                    "source": url
                }
            }
        except Exception as e2:
            print(f"Fallback Extraction Error: {e2}")
            return {"raw_text": "", "metadata": {"source": url}}

def extract_x(url: str) -> dict:
    """Placeholder for X extraction (requires API or specific scrapers)."""
    # For this assessment, we'll return a placeholder or attempt a simple fetch
    return {
        "raw_text": f"X.com content from {url} (Extraction requires specialized tools or API)",
        "metadata": {
            "author": "X User",
            "date": "Unknown",
            "source": url
        }
    }
