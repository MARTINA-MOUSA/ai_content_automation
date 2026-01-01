from typing import TypedDict, Optional

class AgentState(TypedDict):
    url: str
    source_type: str
    raw_text: str
    metadata: dict
    is_ai_news: bool
    analysis_result: dict
    pdf_path: str
    status: str
    error: Optional[str]
