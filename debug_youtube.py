import sys
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi

print(f"Python Executable: {sys.executable}")
print(f"Library File: {youtube_transcript_api.__file__}")
print(f"Library Version: {youtube_transcript_api.__version__ if hasattr(youtube_transcript_api, '__version__') else 'Unknown'}")

try:
    print(f"Has list_transcripts: {hasattr(YouTubeTranscriptApi, 'list_transcripts')}")
    # Try calling it with a dummy ID to see if it exists (it will fail with generic error but verify attribute)
    try:
        YouTubeTranscriptApi.list_transcripts("invalid_id")
    except Exception as e:
        print(f"Call result: {type(e).__name__}: {e}")
except Exception as e:
    print(f"Error checking attribute: {e}")
