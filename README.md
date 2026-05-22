# OpenNotebookLM++

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-CPU-blue.svg)
![Ollama](https://img.shields.io/badge/LLM-Ollama-black.svg)

**OpenNotebookLM++** is a local, highly-secure, multimodal Research Assistant powered by Retrieval-Augmented Generation (RAG). It enables users to securely upload and chat with a wide variety of documents (PDF, TXT, MD) and videos (MP4, MKV). 

Built with an emphasis on data privacy, the application runs entirely on local infrastructure utilizing powerful open-source models, avoiding the need for external API calls for embeddings or generation.

## Features

- **Multimodal Data Ingestion**: Seamlessly upload and index PDFs, Markdown files, Text documents, and Video formats (MP4/MKV).
- **Video & Audio Transcription**: Integrates OpenAI's `Whisper` alongside `FFmpeg` to extract audio from video files and generate precise temporal transcripts.
- **Local RAG Pipeline**: Utilizes local `sentence-transformers` for dense vector embeddings and a blazing-fast `FAISS` vector database for similarity search.
- **Strict Guardrails**: Designed with production-level Q&A guardrails to prevent hallucinations; the LLM strictly refuses to answer if relevant context isn't found.
- **Source Citations**: Answers are backed by precise citations, showing page numbers for PDFs and start/end timestamps for videos.
- **Modern User Interface**: A clean, responsive frontend built with `Streamlit`.
- **High-Performance Backend**: Asynchronous architecture built entirely on `FastAPI`.

---

## Technology Stack

- **Backend Architecture**: FastAPI, Uvicorn, Python 3.9+
- **Frontend / UI**: Streamlit
- **LLM / Inference**: Ollama (`mistral:7b-instruct` or similar)
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Media Processing**: `FFmpeg`, `openai-whisper`, `pypdf`

---

##  Getting Started

### Prerequisites

1. **Python 3.9+** installed on your system.
2. **FFmpeg** installed and added to your system's PATH (required for video transcription).
3. **Ollama** installed and running locally.
   - You must pull an LLM model before running: `ollama run mistral`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/OpenNotebookLM.git
   cd OpenNotebookLM
   ```

2. Create and activate a virtual environment:
   ```powershell
   # On Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

For a hassle-free startup on Windows, simply double click the provided batch script:
- `run_app.bat`

**Manual Startup:**

Open two separate terminals in the project root directory. Ensure the virtual environment is activated in both.

**Terminal 1 (Backend):**
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 (Frontend):**
```bash
streamlit run frontend/app.py
```
The UI will automatically launch in your browser at `http://localhost:8501`.

---

##  Project Architecture

```text
OpenNotebookLM/
├── app/
│   ├── api/                 # FastAPI routers (ingest, query, health)
│   ├── core/                # Configuration and Pydantic settings
│   ├── models/              # Pydantic schema definitions (document, query, video)
│   ├── services/            # Core business logic
│   │   ├── chunker.py           # Text splitting & chunking logic
│   │   ├── embedder.py          # SentenceTransformer wrapping
│   │   ├── guardrails.py        # Validation and anti-hallucination layers
│   │   ├── llm.py               # Local Ollama connection layer
│   │   ├── retriever.py         # FAISS similarity search and context building
│   │   ├── vector_store.py      # FAISS index management
│   │   └── video_loader.py      # Whisper and FFmpeg integration
│   └── main.py              # FastAPI application entry point
├── data/                    # Local storage for uploads and FAISS indexes
├── frontend/
│   └── app.py               # Streamlit application
├── run_app.bat              # Windows startup script
└── requirements.txt         # Project dependencies
```

---

