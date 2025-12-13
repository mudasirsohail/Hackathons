from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.request_models import ChatRequest, ChatResponse, ChatHistoryResponse
from ..services.chat_service import ChatService
from ..vector_store.qdrant_client import QdrantWrapper
from ..services.embedding_service import EmbeddingService
from ..utils.logger import logger
from uuid import UUID


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint - handles both global and selected text modes
    Supports anonymous sessions - creates new session if session_id not provided
    """
    try:
        qdrant_wrapper = QdrantWrapper()
        embedding_service = EmbeddingService()
        chat_service = ChatService(db, qdrant_wrapper, embedding_service)

        # Handle both 'query' (legacy) and 'message' (frontend) fields
        query_text = request.query or request.message
        if not query_text:
            raise HTTPException(
                status_code=400,
                detail="Either 'query' or 'message' field is required"
            )

        # Handle session_id: if invalid or missing, generate a new one
        session_id = None
        if request.session_id:
            try:
                session_id = UUID(request.session_id)
            except ValueError:
                # If the session_id is not a valid UUID, ignore it and create a new session
                logger.warning(f"Invalid session_id format received: {request.session_id}. Creating new session.")
                session_id = None

        user_id = request.user_id

        if request.mode == "selected_text":
            if not request.selected_text:
                raise HTTPException(
                    status_code=400,
                    detail="selected_text is required for selected_text mode"
                )

            result = chat_service.chat_selected_text(
                query=query_text,
                selected_text=request.selected_text,
                session_id=session_id,
                user_id=user_id
            )
        else:  # global mode
            result = chat_service.chat_global(
                query=query_text,
                session_id=session_id,
                user_id=user_id
            )

        # Ensure response always contains the session_id for frontend to track
        response_data = {
            'response': result['response'],
            'context': result['context'],
            'session_id': result['session_id']
        }

        return ChatResponse(**response_data)

    except ValueError as e:
        # Handle specific validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Retrieve chat history for a specific session
    """
    try:
        qdrant_wrapper = QdrantWrapper()
        embedding_service = EmbeddingService()
        chat_service = ChatService(db, qdrant_wrapper, embedding_service)
        
        session_uuid = UUID(session_id)
        
        history = chat_service.get_chat_history(session_uuid)
        
        return ChatHistoryResponse(
            session_id=session_id,
            messages=history
        )
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))