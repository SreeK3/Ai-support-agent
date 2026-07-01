from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Store conversation history
chat_history = []

def create_llm():
    """Create Groq LLM connection."""
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0.3,
    )

def get_response(retriever, question: str) -> dict:
    """
    Send question to AI with relevant document context.
    """
    try:
        # Step 1: Get relevant documents from ChromaDB
        relevant_docs = retriever.invoke(question)
        context = "\n".join([doc.page_content for doc in relevant_docs])

        # Step 2: Build prompt with context + history
        llm = create_llm()
        
        system_prompt = f"""You are Aisu, AsuiTech Solutions' AI assistant. 
You are friendly, professional, and helpful.
Your name is Aisu and you were created for AsuiTech Solutions.

Use the following company information to answer questions accurately.
If the answer is not in the context, say you don't have that information 
but offer to connect them with the AsuiTech support team.

Company Context:
{context}"""

        messages = [("system", system_prompt)]
        
        # Add conversation history
        for msg in chat_history[-6:]:  # last 3 exchanges
            messages.append(msg)
        
        # Add current question
        messages.append(("human", question))

        # Step 3: Get AI response
        response = llm.invoke(messages)
        answer = response.content

        # Step 4: Save to history
        chat_history.append(("human", question))
        chat_history.append(("assistant", answer))

        return {
            "answer": answer,
            "success": True
        }

    except Exception as e:
        return {
            "answer": f"Sorry, I encountered an error: {str(e)}",
            "success": False
        }

if __name__ == "__main__":
    from rag import get_retriever
    print("Testing agent...")
    retriever = get_retriever()
    response = get_response(retriever, "What services does AsuiTech offer?")
    print(f"\nAnswer: {response['answer']}")