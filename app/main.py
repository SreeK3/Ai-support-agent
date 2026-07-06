from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import sys
import os

# Add app directory to path so we can import rag and agent
sys.path.append(str(Path(__file__).parent))

from rag import get_retriever
from agent import get_response
import agent

load_dotenv()

app = FastAPI(
    title="AI Support Agent",
    description="RAG-powered AI assistant for company support",
    version="1.0.0"
)

# Mount frontend folder so browser can access index.html
app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).parent.parent / "frontend")),
    name="static"
)

# Load retriever once when server starts
print("Loading AI agent...")
retriever = get_retriever()
print("AI agent ready!")

# Request model — what browser sends
class QuestionRequest(BaseModel):
    question: str

# Response model — what we send back
class AnswerResponse(BaseModel):
    answer: str
    success: bool

@app.get("/")
def home():
    """Serve the chat UI."""
    return FileResponse(
        str(Path(__file__).parent.parent / "frontend" / "index.html")
    )

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    """
    Receive question from browser,
    send to AI agent,
    return answer.
    """
    if not request.question.strip():
        return AnswerResponse(
            answer="Please ask a question!",
            success=False
        )
    
    response = get_response(retriever, request.question)
    return AnswerResponse(
        answer=response["answer"],
        success=response["success"]
    )

@app.delete("/clear")
def clear_history():
    """Clear conversation history."""
    agent.chat_history.clear()
    return {"message": "Conversation history cleared!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "AI Support Agent"}