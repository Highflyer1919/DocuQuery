# DocuQuery — RAG-Based Document Q&A System

> Upload any PDF and ask questions in natural language. Every answer includes exact page-level citations.
>
> **Live Demo:** [docuquery-u2m7jf6mej5n3lbpbufvkz.streamlit.app](https://docuquery-u2m7jf6mej5n3lbpbufvkz.streamlit.app)

---

## Overview

DocuQuery is a lightweight document question-answering system that lets you chat with any PDF. It retrieves the most relevant sections of the document using BM25 keyword search, passes them as context to an LLM, and returns a direct answer — with the exact page numbers cited under every response.

The system is intentionally constrained to the uploaded document. If the answer isn't in the PDF, it says so rather than hallucinating.

---

## How It Works

```
User uploads PDF
        │
        ▼
PDF parsed into pages → split into overlapping text chunks
        │
        ▼
BM25 index built over all chunks (keyword-based retrieval)
        │
        ▼
User asks a question → BM25 ranks chunks by relevance
        │
        ▼
Top 4 chunks passed as context to Groq LLM
        │
        ▼
Answer returned with 📍 page-level source citation
```

---

## Features

- **PDF upload** — supports any text-based PDF up to dozens of pages
- **Natural language Q&A** — ask anything about the document in plain English
- **Page-level citations** — every answer shows exactly which pages it came from
- **Hallucination mitigation** — model is constrained to document content only; responds with "I couldn't find the answer in the uploaded document" when the information isn't there
- **Chat history** — full conversation persists within the session
- **Clear & reload** — switch documents mid-session with one click

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Interface | Streamlit |
| PDF Parsing | LangChain PyPDFLoader |
| Text Chunking | LangChain RecursiveCharacterTextSplitter |
| Retrieval | BM25 (rank-bm25) |
| LLM | Groq API (openai/gpt-oss-20b) |
| Language | Python |

---

## Project Structure

```
DocuQuery/
├── app.py              ← Streamlit UI and session management
├── rag_pipeline.py     ← PDF processing, BM25 retrieval, LLM answering
├── requirements.txt    ← Python dependencies
└── .env                ← API keys (not committed)
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Highflyer1919/DocuQuery.git
cd DocuQuery

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key (no credit card required) at [console.groq.com](https://console.groq.com).

---

## Usage

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser. Upload a PDF in the sidebar and start asking questions.

---

## Known Limitations

- **Keyword-based retrieval** — BM25 matches exact keywords, so synonym gaps (e.g. asking "testing" when the document says "evaluation") may cause misses. Semantic embedding-based retrieval would address this.
- **Text PDFs only** — scanned or image-based PDFs are not supported without an OCR layer.
- **Session-only memory** — chat history resets on page refresh.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
