import os
from dotenv import load_dotenv
from app.graph.workflow import graph_app

load_dotenv()

def test_single():
    url = "https://techcrunch.com/2024/05/13/openai-launches-gpt-4o-a-faster-multimodal-ai-model-thats-free-for-all-users/"
    print(f"Testing URL: {url}")
    initial_state = {
        "url": url,
        "source_type": "",
        "raw_text": "",
        "metadata": {},
        "is_ai_news": False,
        "analysis_result": {},
        "pdf_path": "",
        "status": "starting",
        "error": None
    }
    
    final_state = graph_app.invoke(initial_state)
    print(f"Is AI News: {final_state.get('is_ai_news')}")
    if final_state.get('is_ai_news'):
        print(f"Title: {final_state['analysis_result'].get('title')}")
        print(f"PDF Generated: {os.path.exists(final_state.get('pdf_path', ''))}")

if __name__ == "__main__":
    test_single()
