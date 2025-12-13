from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from ..database.schemas import ChatSession, ChatMessage
from ..vector_store.qdrant_client import QdrantWrapper
from ..services.embedding_service import EmbeddingService
from ..config.settings import settings
from ..utils.logger import logger


def create_rag_prompt(context_str: str, query: str) -> str:
    """
    Create a properly formatted RAG prompt that instructs the LLM to use the provided context
    """
    if context_str.strip():
        # If we have context, use it
        return f"""You are an AI assistant helping users with information from documentation.
    Answer the user's question based ONLY on the provided context.
    If the context doesn't contain relevant information, clearly state that you don't have enough information to answer.

    CONTEXT:
    {context_str}

    QUESTION:
    {query}

    ANSWER:"""
    else:
        # If no context is available, create a prompt without context
        return f"""You are an AI assistant helping users with information from documentation.
    The system tried to find relevant context for the user's question but couldn't find any relevant information.
    Try to answer the user's question based on your general knowledge, but acknowledge that you don't have specific documentation context.

    QUESTION:
    {query}

    ANSWER:"""


def validate_chat_mode(mode: str) -> bool:
    """
    Validate that the chat mode is one of the supported modes
    """
    return mode in ["global", "selected_text"]


def extract_chat_history_for_llm(db: Session, session_id: UUID) -> List[Dict[str, str]]:
    """
    Extract chat history in a format suitable for the LLM
    """
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp.asc()).all()
    
    # Convert to the format expected by the LLM
    formatted_history = []
    for msg in messages:
        formatted_history.append({
            'role': msg.role,
            'content': msg.content
        })
    
    return formatted_history