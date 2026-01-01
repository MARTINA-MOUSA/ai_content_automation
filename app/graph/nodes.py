from app.graph.state import AgentState
from app.services.content_fetcher import extract_blog, extract_youtube, extract_x
from app.services.ai_service import validate_ai_news, analyze_content_structured
from app.services.pdf_service import generate_pdf_report
import os
import uuid

# NODE 1 — Input Node
def input_node(state: AgentState):
    print(">>> [Node 1] Input")
    return {"status": "input_received"}

# NODE 2 — Source Detection Node
def source_detection_node(state: AgentState):
    print(">>> [Node 2] Source Detection")
    url = state["url"].lower()
    if "youtube.com" in url or "youtu.be" in url:
        source_type = "youtube"
    elif "x.com" in url or "twitter.com" in url:
        source_type = "x"
    else:
        source_type = "blog"
    return {"source_type": source_type}

# NODE 3 — Content Extraction Node
def extraction_node(state: AgentState):
    print(">>> [Node 3] Extraction")
    url = state["url"]
    source_type = state["source_type"]
    
    if source_type == "youtube":
        data = extract_youtube(url)
    elif source_type == "x":
        data = extract_x(url)
    else:
        data = extract_blog(url)
        
    return {
        "raw_text": data["raw_text"],
        "metadata": data["metadata"]
    }

# NODE 4 — AI News Validation Node (Gemini)
def validation_node(state: AgentState):
    print(">>> [Node 4] Validation")
    is_ai_news = validate_ai_news(state["raw_text"])
    return {"is_ai_news": is_ai_news}

# NODE 5 — Gemini Analysis Node
def analysis_node(state: AgentState):
    print(">>> [Node 5] Analysis")
    if not state.get("is_ai_news", False):
        return {"status": "skipped_not_ai"}
    
    analysis = analyze_content_structured(state["raw_text"])
    return {"analysis_result": analysis}

# NODE 6 — Report Assembly Node
def report_assembly_node(state: AgentState):
    print(">>> [Node 6] Report Assembly")
    if not state.get("is_ai_news", False):
        return {}
        
    # Combine metadata and analysis
    report = state["analysis_result"].copy()
    report["metadata"] = state["metadata"]
    report["url"] = state["url"]
    return {"analysis_result": report}

# NODE 7 — PDF Generator Node
def pdf_generator_node(state: AgentState):
    print(">>> [Node 7] PDF Generation")
    if not state.get("is_ai_news", False):
        return {}
        
    os.makedirs("output", exist_ok=True)
    filename = f"report_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join("output", filename)
    
    pdf_path = generate_pdf_report(state["analysis_result"], state["metadata"], output_path)
    return {"pdf_path": pdf_path}

# NODE 8 — Output Node
def output_node(state: AgentState):
    print(">>> [Node 8] Output")
    if not state.get("is_ai_news", False):
        return {"status": "completed", "error": "Content is not related to AI News."}
    return {"status": "completed"}


