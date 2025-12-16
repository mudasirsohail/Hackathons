"""
Hugging Face Spaces compatibility entry point
This file provides a direct reference to the FastAPI app for Hugging Face Spaces
"""
from app.main import app

# This allows Hugging Face Spaces to directly reference the app
# Usage: gradio would use this, but since we're using FastAPI directly,
# Hugging Face will run this with uvicorn
if __name__ == "__main__":
    import uvicorn
    import os
    
    # Hugging Face Spaces provides a PORT environment variable
    port = int(os.getenv("PORT", 7860))
    
    # Run with uvicorn
    uvicorn.run(
        "app.py:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )