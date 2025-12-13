from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime


# User Models
class UserCreate(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# Document Models
class DocumentCreate(BaseModel):
    title: str
    source_path: str
    content: str
    checksum: str


class DocumentResponse(BaseModel):
    id: UUID
    title: str
    source_path: str
    checksum: str
    version: int
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentIngestResponse(BaseModel):
    document_id: str
    status: str
    chunks_created: Optional[int] = None
    message: str


# Chat Models
class ChatRequest(BaseModel):
    query: Optional[str] = None  # Keep for backward compatibility
    message: Optional[str] = None  # New field for frontend compatibility
    session_id: Optional[str] = None  # String to allow any format, validate in endpoint
    user_id: Optional[int] = None
    mode: str = "global"  # "global" or "selected_text"
    selected_text: Optional[str] = None  # Used when mode is "selected_text"


class ChatResponse(BaseModel):
    response: str
    context: List[Dict[str, Any]]
    session_id: str


class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]]


# Query Models
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class QueryResponse(BaseModel):
    results: List[Dict[str, Any]]


# Ingestion Models
class IngestDocumentsRequest(BaseModel):
    documents: List[DocumentCreate]


class BulkIngestResponse(BaseModel):
    results: List[DocumentIngestResponse]