from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .logger import logger


def add_exception_handlers(app: FastAPI):
    """Add global exception handlers to the FastAPI application"""
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions"""
        logger.error(f"HTTP error {exc.status_code} for request {request.url}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors"""
        logger.error(f"Validation error for request {request.url}: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Validation error",
                "details": exc.errors()
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions"""
        logger.error(f"General error for request {request.url}: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error"}
        )


def setup_error_handling(app: FastAPI):
    """Setup error handling and response formatting for the application"""
    
    # Add custom middleware for request logging
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all incoming requests"""
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response