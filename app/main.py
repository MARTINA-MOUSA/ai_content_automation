from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from app.graph.workflow import graph_app
import uvicorn

app = FastAPI(title="AI Content Automation", version="1.0")

class AnalyzeRequest(BaseModel):
    url: str

def run_automation_task(request: AnalyzeRequest):
    """
    Runs the LangGraph workflow.
    """
    initial_state = {
        "url": request.url,
        "source_type": "",
        "raw_text": "",
        "metadata": {},
        "is_ai_news": False,
        "analysis_result": {},
        "pdf_path": "",
        "status": "starting",
        "error": None
    }
    
    print(f"Starting job for {request.url}")
    # Invoke the graph
    result = graph_app.invoke(initial_state)
    print(f"Job finished. Final status: {result.get('status')} Error: {result.get('error')}")

@app.post("/webhook")
async def analyze_content(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    """
    Receives a URL, returns immediately, and processes in background.
    """
    background_tasks.add_task(run_automation_task, request)
    return {"message": "Request received. Processing started.", "url": request.url}

@app.get("/")
def root():
    return {"status": "ok", "service": "AI Content Automation Agent"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
