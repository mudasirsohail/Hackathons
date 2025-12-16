from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key:
    client = Groq(api_key=groq_api_key)
else:
    client = None

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]


@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Simple chat endpoint without RAG, database, or history features.
    """
    try:
        message = request.message

        if not message.strip():
            raise ValueError("Message cannot be empty")

        if client is None:
            return ChatResponse(
                response="Error: GROQ_API_KEY is not set in environment variables.",
                sources=[]
            )

        # Generate response using Groq
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a robotics book titled \"Physical AI & Humanoid Robotics\"."},
                {"role": "user", "content": message}
            ]
        )

        response_text = completion.choices[0].message.content

        return ChatResponse(
            response=response_text,
            sources=[]  # Empty since we're not using RAG
        )
    except Exception as e:
        raise e