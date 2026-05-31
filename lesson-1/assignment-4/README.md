# Assignment-4: RAG System for Corporate Policies

## Objective & Overview
The objective of this assignment is to build a production-grade, layered **Retrieval-Augmented Generation (RAG)** application. This tool allows employees to ask natural language questions about corporate policies and receive highly accurate, context-grounded answers. 

### Application Demo Video

[![Watch the RAG System Demo](https://shields.io▶_Watch_Demo-Click_to_Play_Video-success?style=for-the-badge&logo=quicktime)](https://github.com)

*If the video player does not stream directly in your browser, you can download the recording directly via this **[Direct Video File Link](https://github.com)**.*


To achieve high speed and premium response quality, the application decouples vector generation from logical synthesis:
* **Vector Embeddings (Local)**: Generated using a local Ollama instance running the lightweight `tinyllama:latest` model.
* **Vector Store**: Persisted locally in a persistent **ChromaDB** database.
* **Reasoning & Synthesis (Cloud)**: Performed using the ultra-fast **Groq Cloud API** running `llama-3.1-8b-instant` with a 2048 token limit for detailed, comprehensive answers.
* **Frontend**: A sleek, dark-themed Streamlit interface.

---

## Requirements & Prerequisites
Ensure the following are installed and configured:
1. **Python**: Version 3.11 recommended.
2. **Ollama**: Local LLM host.
3. **Local Embedder**: Ensure the local embedder model is pulled:
   ```bash
   ollama pull tinyllama:latest
   ```
4. **Groq Cloud API Key**: A valid API Key from Groq Cloud Console.

---

## Setup & Running Instructions

### 1. Install Dependencies
Navigate to the assignment folder and install the requirements:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a file named `.env` in the assignment root directory (`lesson-1/assignment-4/`):
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 3. Run the Streamlit Application
Start the server:
```bash
streamlit run app.py
```
This will start the local server and automatically launch the dashboard in your web browser at `http://localhost:8501`.

### 4. Upload and Index Policies
* In the sidebar under **Ingest Documents**, click the file uploader.
* Select `sample/company_policy.txt` (or any other PDF, TXT, or DOCX document).
* Click the **Process & Embed Documents** button. The document will be parsed, embedded, and added to your ChromaDB instance.
* Once completed, you will see `company_policy.txt` listed under **Currently Indexed Documents**.

---

## Codebase Architecture & File Layering

This application is built with a modular, layered codebase following professional separation of concerns:

```
lesson-1/assignment-4/
│
├── .env                  # Configuration keys (excluded from source control)
├── requirements.txt      # Dependency configurations
├── app.py                # Frontend Streamlit presentation layer & UI logic
├── rag_processor.py      # Orchestration layer (glues database, parsing, and LLM layers)
├── llm.py                # LLM connectors (local embeddings & Groq API requests)
├── database.py           # Database interactions (ChromaDB vectors query & add)
├── parsers.py            # File ingestion parser layer (PDF page split, DOCX grouping, TXT split)
└── sample/
    └── company_policy.txt # Vast, detailed policy text file
```

### Layer Descriptions:
1. **File Parser Layer (`parsers.py`)**:
   * Extracts clean text and attaches metadata locations.
   * `parse_txt_chunks`: Splits text by double-newlines.
   * `parse_pdf_pages`: Page-level splitting utilizing `pypdf`.
   * `parse_docx_paragraphs`: Groups Word paragraphs into blocks of 3 to avoid tiny fragments.
2. **Database Layer (`database.py`)**:
   * Creates a local, persistent client in `chroma_db/`.
   * Manages similarity retrieval using vector representations, fetching the top `K` most relevant chunks.
3. **LLM Connection Layer (`llm.py`)**:
   * `get_embedding`: Fetches local embeddings from Ollama (`tinyllama:latest`).
   * `query_llm`: Connects to Groq Cloud endpoint (`llama-3.1-8b-instant`) with `max_tokens=2048` to allow comprehensive explanations without truncation.
4. **Orchestrator Layer (`rag_processor.py`)**:
   * Standardizes document flow from file paths to database chunks.
   * **Clean Re-Ingestion**: Deletes any existing database records matching the file source name before inserting new ones. This prevents stale duplicates.
   * Generates context-grounded system prompts and prohibits markdown italics (`*` or `_`) for clean output rendering.
5. **UI Layer (`app.py`)**:
   * Premium styled glassmorphism dark-mode UI.
   * **Two-Stage Execution Engine**: Streamlit runs script execution from top-to-bottom. To disable user inputs and change the button label to "Processing" during slow API calls, the app records states in `st.session_state` and triggers reruns.

---

## Detailed RAG Execution Lifecycle

```
[User inputs Question]
         │
         ▼
[Stage 1: Form Clicked]
 ├── Set st.session_state.processing = True
 ├── Set st.session_state.query_to_run = query
 └── Call st.rerun()  <-- Restarts script to update visual button states
         │
         ▼
[Stage 2: Script Reruns]
 ├── Render form as disabled (shows greyed out inputs & "Processing" button)
 ├── Enter st.spinner context block
 │    ├── Call rag_processor.query_rag()
 │    │    ├── Embed query (Ollama)
 │    │    ├── Similarity search (ChromaDB)
 │    │    ├── Build context-grounded prompt
 │    │    └── Run inference (Groq Cloud API)
 │    └── Save output to st.session_state.last_answer
 ├── Finally Block:
 │    ├── Set processing = False, query_to_run = None
 │    └── Call st.rerun()  <-- Restarts script to restore form states
         │
         ▼
[Stage 3: Page Rendering]
 ├── Render form as enabled (ready for next prompt)
 └── Display the Answer & Citations dynamically
```

This sequence provides a fluid user experience: inputs are locked to prevent double-clicks, the status spinner is visible in real-time, and the final state is cleanly restored for the next question.
