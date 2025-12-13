"""
Fully Working FastAPI Backend for Chatbot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastAPI app - ONLY ONE instance
app = FastAPI(
    title="Chatbot API",
    description="Simple chatbot API with proper CORS",
    version="1.0.0"
)

# Apply CORS middleware - DO THIS BEFORE ANY ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Docusaurus default
        "http://localhost:3001",    # Your frontend port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://0.0.0.0:3000",
        "http://0.0.0.0:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Request and Response Models
class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    """Root endpoint for testing"""
    logger.info("Root endpoint accessed")
    return {"message": "Chatbot API is running!"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that accepts JSON and returns a response
    """
    try:
        logger.info(f"Received message: {request.message}")
        logger.info(f"Context provided: {bool(request.context)}")

        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message is required")

        # Simple echo response - replace with your actual chatbot logic
        response_text = f"You said: {request.message}"
        
        logger.info(f"Generated response: {response_text}")
        
        return ChatResponse(response=response_text)
        
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        # Log and return a meaningful error response
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server on port 8001")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )