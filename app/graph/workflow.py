from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.nodes import (
    input_node,
    source_detection_node,
    extraction_node,
    validation_node,
    analysis_node,
    report_assembly_node,
    pdf_generator_node,
    output_node
)

def should_continue(state: AgentState):
    if state.get("is_ai_news"):
        return "analyze"
    return END

def build_graph():
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("input", input_node)
    workflow.add_node("detect_source", source_detection_node)
    workflow.add_node("extract", extraction_node)
    workflow.add_node("validate", validation_node)
    workflow.add_node("analyze", analysis_node)
    workflow.add_node("assemble", report_assembly_node)
    workflow.add_node("generate_pdf", pdf_generator_node)
    workflow.add_node("output", output_node)

    # Define edges
    workflow.set_entry_point("input")
    workflow.add_edge("input", "detect_source")
    workflow.add_edge("detect_source", "extract")
    workflow.add_edge("extract", "validate")
    
    # Conditional edge: Stop if not AI news
    workflow.add_conditional_edges(
        "validate",
        should_continue,
        {
            "analyze": "analyze",
            END: END
        }
    )
    
    workflow.add_edge("analyze", "assemble")
    workflow.add_edge("assemble", "generate_pdf")
    workflow.add_edge("generate_pdf", "output")
    workflow.add_edge("output", END)

    return workflow.compile()

# Singleton instance
graph_app = build_graph()
