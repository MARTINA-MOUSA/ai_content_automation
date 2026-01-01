# AI Content Analysis System

An end-to-end system for analyzing content (Blog posts, YouTube videos, X.com posts) using **LangGraph** orchestration and **Google Gemini** LLM. The system validates if the content is related to AI News before performing a detailed analysis and generating a professional PDF report.

---

## 🛠️ Tech Stack
- **Python**
- **LangGraph** (Orchestration)
- **Google Gemini** (LLM - gemini-2.5-flash)
- **Streamlit** (User Interface)
- **FastAPI** (Backend Service)
- **ReportLab** (PDF Generation)
- **Newspaper3k** (Web Scraping)

---

## 🚀 Getting Started

### 1. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API Key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Running the System

#### Option A: Running the UI (Streamlit)
To launch the user-friendly interface:
```bash
streamlit run app_ui.py
```

#### Option B: Running the Backend (FastAPI API)
To run the API service (e.g., for webhook integrations):
```bash
python -m app.main
```
The API will be available at `http://localhost:8000`. You can test the analysis endpoint via POST:
```bash
curl -X POST http://localhost:8000/webhook -H "Content-Type: application/json" -d '{"url": "https://techcrunch.com/2024/05/13/openai-launches-gpt-4o-a-faster-multimodal-ai-model-thats-free-for-all-users/"}'
```

---

## ✨ Features
- **Intelligent Source Detection**: Automatically handles YouTube, X, and Blog URLs.
- **AI-Driven Validation**: Only processes content if it is identified as AI-related news.
- **Advanced Analysis**: Generates structured summaries, extracts key topics, and determines sentiment.
- **Automated PDF Reports**: High-quality downloadable reports with metadata and analysis.
- **Modular Pipeline**: Each step is a LangGraph node, ensuring clean and scalable logic.
