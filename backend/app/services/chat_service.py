from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..database.schemas import ChatSession, ChatMessage
from ..vector_store.qdrant_client import QdrantWrapper
from ..services.embedding_service import EmbeddingService
from ..config.settings import settings
from ..utils.logger import logger
from ..utils.helpers import create_rag_prompt, extract_chat_history_for_llm
from groq import Groq
from app.config.settings import settings


class ChatService:
    def __init__(self, db: Session, qdrant_wrapper: QdrantWrapper, embedding_service: EmbeddingService):
        self.db = db
        self.qdrant = qdrant_wrapper
        self.embedding_service = embedding_service

        # Initialize Groq client if API key is available
        if settings.GROQ_API_KEY:
            self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
            logger.info(f"Configured Groq with API key: {bool(settings.GROQ_API_KEY)}")
            logger.info(f"Using model for Groq: {settings.CHAT_MODEL}")
        else:
            logger.warning("GROQ_API_KEY not provided")
            self.groq_client = None

        # Set OpenAI API key if available
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY

    def create_session(self, user_id: int, title: str = None) -> ChatSession:
        """Create a new chat session"""
        # For anonymous users (user_id = 0), we'll still create a session but note that it's anonymous
        session = ChatSession(
            user_id=user_id if user_id != 0 else None,  # Store as NULL in DB for anonymous users
            session_title=title or "New Chat Session"
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_relevant_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from vector store based on the query
        Args:
            query: User query to find relevant context for
            top_k: Number of top relevant chunks to retrieve
        Returns:
            List of relevant context chunks
        """
        # Embed the query
        query_embedding = self.embedding_service.embed_text(query)

        # Search in Qdrant for similar chunks
        results = self.qdrant.search_similar(query_embedding, top_k=top_k)

        return results

    def get_selected_text_context(self, selected_text: str) -> List[Dict[str, Any]]:
        """
        Retrieve context specifically from user-selected text
        Args:
            selected_text: The text the user highlighted/selected
        Returns:
            List containing the selected text as context
        """
        # Just return the selected text as the context
        return [{
            'id': 'selected_text',
            'text': selected_text,
            'metadata': {'source': 'user_selection'},
            'score': 1.0
        }]

    def generate_response(self, query: str, context: List[Dict[str, Any]], chat_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response using the LLM based on the query and context
        Args:
            query: User's question
            context: Relevant context retrieved from vector store
            chat_history: Previous conversation history
        Returns:
            Generated response from the LLM
        """
        # Prepare the context text
        context_texts = [item['text'] for item in context]
        context_str = "\n\n".join(context_texts)

        # Create RAG prompt
        rag_prompt = create_rag_prompt(context_str, query)

        try:
            # Check if using Groq model
            if settings.CHAT_MODEL and self.groq_client:
                # Create the full prompt by combining context and the user query
                # Include chat history in the prompt for context
                full_prompt = rag_prompt
                if chat_history and len(chat_history) > 0:
                    history_text = "\nPrevious conversation:\n"
                    for msg in chat_history:
                        role = "User" if msg['role'] == 'user' else "Assistant"
                        history_text += f"{role}: {msg['content']}\n"
                    full_prompt = history_text + "\n\n" + rag_prompt

                # Prepare messages for Groq
                messages = [{"role": "user", "content": full_prompt}]

                # Generate response using Groq
                logger.info(f"Calling Groq with model: {settings.CHAT_MODEL}")
                response = self.groq_client.chat.completions.create(
                    model=settings.CHAT_MODEL,
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7
                )

                logger.info(f"Groq response received successfully")
                return response.choices[0].message.content.strip()

            # Otherwise, use OpenAI model
            else:
                if not settings.OPENAI_API_KEY:
                    raise ValueError("OPENAI_API_KEY is required for OpenAI models")

                # Prepare messages for the LLM
                messages = [{"role": "user", "content": rag_prompt}]

                # Add chat history if provided (to maintain conversational context)
                if chat_history:
                    # Use the first message as system prompt if it doesn't exist in current call
                    # Otherwise, append the conversation history
                    messages = chat_history + messages

                # Initialize the OpenAI client
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

                # Call the LLM
                response = client.chat.completions.create(
                    model=settings.CHAT_MODEL,
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7
                )

                return response.choices[0].message.content.strip()

        except Exception as e:
            # Log the full exception details for debugging
            import traceback
            logger.error(f"Full exception traceback for LLM call: {traceback.format_exc()}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception message: {str(e)}")

            # Check if it's a Groq-related error
            if "groq" in str(e).lower() or "404" in str(e):
                # Don't mislead user by blaming API key unless it's actually missing
                if not self.groq_client:
                    logger.error("Groq client is not configured (missing API key)")
                    return "Sorry, the Groq API is not configured. Please set GROQ_API_KEY in your environment."
                else:
                    logger.error("Groq API error (not an API key issue)")
                    return "Sorry, I encountered an issue with the AI service. Please check the backend logs for details."
            else:
                # Other LLM errors
                return "Sorry, I encountered an error while generating a response."
    
    def save_message(self, session_id: UUID, role: str, content: str, context_used: List[Dict[str, Any]] = None) -> ChatMessage:
        """Save a message to the chat history"""
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            context_used=context_used
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_chat_history(self, session_id: UUID) -> List[Dict[str, Any]]:
        """Retrieve chat history for a session"""
        messages = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.timestamp.asc()).all()
        
        return [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat() if msg.timestamp else None
            }
            for msg in messages
        ]
    
    def chat_global(self, query: str, session_id: UUID = None, user_id: int = None) -> Dict[str, Any]:
        """
        Handle global chat (uses all book knowledge)
        Args:
            query: User's question
            session_id: Existing session ID (optional, creates new if not provided)
            user_id: User ID for creating a new session (optional, for anonymous if not provided)
        Returns:
            Dictionary with response and metadata
        """
        # Get or create session
        if not session_id:
            # For anonymous users, create a new session without user association
            session = self.create_session(user_id or 0, title=query[:50])  # Use 0 as placeholder for anonymous
            session_id = session.id
        else:
            session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if not session:
                # If session doesn't exist, create a new one with the given session_id
                session = ChatSession(
                    id=session_id,
                    user_id=user_id or 0,  # Use 0 as placeholder for anonymous
                    session_title=query[:50]
                )
                self.db.add(session)
                self.db.commit()

        # Get relevant context from all documents
        context = self.get_relevant_context(query, top_k=5)

        # Get chat history for context
        chat_history = self.get_chat_history(session_id)

        # Generate response
        response = self.generate_response(query, context, chat_history)

        # Save user message
        self.save_message(session_id, 'user', query, [c['id'] for c in context])

        # Save AI response
        self.save_message(session_id, 'assistant', response, [c['id'] for c in context])

        return {
            'response': response,
            'context': context,
            'session_id': str(session_id)
        }
    
    def chat_selected_text(self, query: str, selected_text: str, session_id: UUID = None, user_id: int = None) -> Dict[str, Any]:
        """
        Handle selected text chat (answers only from user-selected text)
        Args:
            query: User's question about the selected text
            selected_text: The text the user highlighted
            session_id: Existing session ID (optional, creates new if not provided)
            user_id: User ID for creating a new session (optional, for anonymous if not provided)
        Returns:
            Dictionary with response and metadata
        """
        # Get or create session
        if not session_id:
            # For anonymous users, create a new session without user association
            session = self.create_session(user_id or 0, title=f"Focused: {query[:30]}...")
            session_id = session.id
        else:
            session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if not session:
                # If session doesn't exist, create a new one with the given session_id
                session = ChatSession(
                    id=session_id,
                    user_id=user_id or 0,  # Use 0 as placeholder for anonymous
                    session_title=f"Focused: {query[:30]}..."
                )
                self.db.add(session)
                self.db.commit()

        # Use only the selected text as context
        context = self.get_selected_text_context(selected_text)

        # Get chat history for context
        chat_history = self.get_chat_history(session_id)

        # Generate response
        response = self.generate_response(query, context, chat_history)

        # Save user message
        self.save_message(session_id, 'user', query, ['selected_text'])

        # Save AI response
        self.save_message(session_id, 'assistant', response, ['selected_text'])

        return {
            'response': response,
            'context': context,
            'session_id': str(session_id)
        }