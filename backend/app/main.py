from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import ingest, chat
from .config.settings import settings
from .utils.logger import logger
from .utils.error_handlers import add_exception_handlers, setup_error_handling
from .database.db import engine
from .database.schemas import Base
import uvicorn


def create_app():
    app = FastAPI(
        title="Docusaurus RAG Chatbot API",
        description="API for RAG chatbot integrated with Docusaurus documentation",
        version="1.0.0",
        # Add custom error responses
        responses={
            400: {"description": "Bad Request"},
            404: {"description": "Not Found"},
            422: {"description": "Validation Error"},
            500: {"description": "Internal Server Error"}
        }
    )

    # Log runtime configuration at startup
    logger.info(f"GROQ_API_KEY loaded: {bool(settings.GROQ_API_KEY)}")
    logger.info(f"Using LLM model: {settings.CHAT_MODEL}")

    # Log the Groq version
    try:
        import groq
        logger.info(f"Groq SDK version: {groq.__version__}")
    except ImportError:
        logger.warning("Groq SDK not installed")

    # Create all tables on startup (if they don't exist)
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")

    # Log which LLM model is being used
    logger.info(f"Final LLM model: {settings.CHAT_MODEL}")

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8000"],  # Allow specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex="https://.*\.netlify\.app",  # Allow Netlify deployments if needed
    )

    # Setup error handling
    add_exception_handlers(app)
    setup_error_handling(app)

    # Include routers
    app.include_router(ingest.router)
    app.include_router(chat.router)

    @app.get("/")
    def read_root():
        return {"message": "Docusaurus RAG Chatbot API is running!"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "Docusaurus RAG API"}

    return app


app = create_app()


if __name__ == "__main__":
    logger.info("Starting Docusaurus RAG Chatbot API server...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Set to False in production
    )