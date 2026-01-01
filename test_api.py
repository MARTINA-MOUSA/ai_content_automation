import requests
import time

def test_webhook():
    url = "http://localhost:8000/webhook"
    
    # Example Payload
    payload = {
        "url": "https://techcrunch.com/2025/12/29/2025-was-the-year-ai-got-a-vibe-check/",
        "whatsapp_number": "+201229890339"
    }

    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
        print("\nNow check the server logs for background processing...")
    except Exception as e:
        print(f"Failed to connect: {e}")
        print("Make sure the server is running (python -m uvicorn app.main:app)")

if __name__ == "__main__":
    test_webhook()
