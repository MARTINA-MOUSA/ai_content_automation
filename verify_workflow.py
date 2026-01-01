import os
from dotenv import load_dotenv
from app.graph.workflow import graph_app

load_dotenv()

def test_workflow(url):
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
    
    try:
        final_state = graph_app.invoke(initial_state)
        print(f"Status: {final_state.get('status')}")
        print(f"Is AI News: {final_state.get('is_ai_news')}")
        if final_state.get("is_ai_news"):
            print(f"Title: {final_state['analysis_result'].get('title')}")
            print(f"PDF Path: {final_state.get('pdf_path')}")
        else:
            print("Validation works: Content correctly identified as NOT AI News.")
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    # Test 1: AI News (TechCrunch)
    test_workflow("https://techcrunch.com/2024/05/13/openai-launches-gpt-4o-a-faster-multimodal-ai-model-thats-free-for-all-users/")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Non-AI News (BBC Sports - placeholder)
    test_workflow("https://www.bbc.com/sport/football/articles/c981881lx8zo")
