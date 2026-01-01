import streamlit as st
import os
from app.graph.workflow import graph_app

# --- UI Configuration ---
st.set_page_config(
    page_title="AI Content Analyzer",
    page_icon="🤖",
    layout="wide",
)

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1A73E8;
        color: white;
        font-weight: bold;
    }
    .report-card {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI Content Analysis System")
st.markdown("Analyze blog posts, YouTube videos, or X.com posts for **AI-related insights**.")

# --- Sidebar ---
with st.sidebar:
    st.header("About")
    st.info("This system uses LangGraph and Google Gemini to extract, validate, and analyze content related to Artificial Intelligence.")
    st.markdown("---")
    st.markdown("### Supported Sources")
    st.write("✅ Blog Posts (URL)")
    st.write("✅ YouTube Videos")
    st.write("✅ X.com (Twitter) Posts")

# --- Input Section ---
url = st.text_input("Enter Content URL (YouTube, X, or Blog):", placeholder="https://example.com/ai-news")
analyze_button = st.button("Analyze Content")

if analyze_button:
    if not url:
        st.warning("Please enter a URL first.")
    else:
        with st.spinner("🚀 AI Agent is working..."):
            # Initial state
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
            
            # Run LangGraph workflow
            try:
                final_state = graph_app.invoke(initial_state)
                
                if final_state.get("error"):
                    st.error(f"❌ {final_state['error']}")
                elif not final_state.get("is_ai_news"):
                    st.warning("⚠️ This content does not appear to be related to AI News. Analysis skipped.")
                else:
                    # Success Display
                    st.balloons()
                    analysis = final_state["analysis_result"]
                    metadata = final_state["metadata"]
                    
                    st.markdown("---")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader(analysis.get("title", "Analysis Result"))
                        st.markdown(f"**Sentiment:** `{analysis.get('sentiment', 'NEUTRAL').upper()}`")
                        st.write(analysis.get("summary", "No summary provided."))
                        
                        st.markdown("### Key Topics")
                        for topic in analysis.get("key_topics", []):
                            st.markdown(f"- {topic}")
                            
                    with col2:
                        st.markdown('<div class="report-card">', unsafe_allow_html=True)
                        st.markdown("### Metadata")
                        st.write(f"**Author:** {metadata.get('author', 'Unknown')}")
                        st.write(f"**Date:** {metadata.get('date', 'Unknown')}")
                        st.write(f"**Source:** {metadata.get('source', 'Link')}")
                        
                        if final_state.get("pdf_path") and os.path.exists(final_state["pdf_path"]):
                            with open(final_state["pdf_path"], "rb") as f:
                                st.download_button(
                                    label="📥 Download PDF Report",
                                    data=f,
                                    file_name=os.path.basename(final_state["pdf_path"]),
                                    mime="application/pdf"
                                )
                        st.markdown('</div>', unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                print(f"Graph Execution Error: {e}")

st.markdown("---")
st.caption("Powered by LangGraph & Google Gemini 1.5 Flash")
