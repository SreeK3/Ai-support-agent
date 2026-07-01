# Aisu — AI Support Agent

An enterprise-ready RAG-based AI support agent that ingests company documents and answers customer and employee questions intelligently using LangChain, ChromaDB, and Groq LLM — deployed with a real-time chat web UI via FastAPI.

## What is Aisu?

Aisu is a reusable AI Support Agent built for AsuiTech Solutions. It uses **Retrieval Augmented Generation (RAG)** to read company documents and generate accurate, context-aware responses — not generic AI answers.

## How it works

```
User types question in chat UI
        ↓
FastAPI receives the question
        ↓
ChromaDB searches company documents for relevant context
        ↓
Groq LLM (Llama 3) generates an accurate answer
        ↓
Answer displayed in real-time chat interface
```

## Features

- 🔍 **RAG Architecture** — answers from your actual company documents, not generic AI
- 💬 **Real-time Chat UI** — clean browser-based interface
- 🧠 **Conversation Memory** — remembers context across messages
- 📄 **Multi-document support** — ingest PDF and TXT files
- ⚡ **Fast responses** — powered by Groq's ultra-fast inference
- 🔌 **Plug and play** — swap any company's documents and it's ready

## Tech Stack

`Python` · `LangChain` · `ChromaDB` · `Groq API (Llama 3)` · `FastAPI` · `Uvicorn` · `HuggingFace Embeddings` · `Pydantic`

## Project Structure

```
ai-support-agent/
├── app/
│   ├── agent.py          # AI brain — connects Groq LLM + RAG
│   ├── rag.py            # Document ingestion + ChromaDB vector store
│   └── main.py           # FastAPI server + chat endpoints
├── docs/                 # Company documents (TXT, PDF)
├── frontend/
│   └── index.html        # Real-time chat UI
├── chroma_db/            # Vector store (auto-generated)
├── .env                  # API keys (never committed)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/SreeK3/Ai-support-agent.git
cd Ai-support-agent

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
# Create a .env file and add:
GROQ_API_KEY=your_groq_api_key_here

# 5. Add your company documents
# Place .txt or .pdf files in the docs/ folder

# 6. Run the server
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000** for the chat UI.

Get a free Groq API key at **console.groq.com**

## Example Questions

- "What services do you offer?"
- "How can I contact support?"
- "Do you offer free consultations?"
- "What industries do you serve?"

## Evaluation

The RAG pipeline retrieves top-3 most relevant document chunks per query using semantic similarity search with `all-MiniLM-L6-v2` embeddings stored in ChromaDB.

## Built For

Originally built as an AI support assistant for **AsuiTech Solutions** — reusable for any company by replacing documents in the `docs/` folder.
