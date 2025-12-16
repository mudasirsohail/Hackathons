from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat
import os


app = FastAPI(
    title="Simple Chatbot API",
    description="Simple API for chatbot without database or vector store dependencies",
    version="1.0.0",
)


# Add CORS middleware with configurations suitable for Hugging Face Spaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Hugging Face Spaces compatibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only chat router (no database dependencies)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Simple Chatbot API is running!"}

@app.get("/health")
async def health_check():
    # Simple health check - no DB dependencies
    return {"status": "healthy", "service": "Simple Chat API"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Use PORT environment variable for Hugging Face
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Set to False in production
    )