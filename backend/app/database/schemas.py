from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to chat sessions
    chat_sessions = relationship("ChatSession", back_populates="user", lazy="select")


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    source_path = Column(Text, nullable=False)  # Path to the .md/.mdx file
    checksum = Column(String(255))  # To detect changes
    version = Column(Integer, default=1)
    doc_metadata = Column(JSON)  # Extra metadata from docusaurus
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to document chunks
    chunks = relationship("DocumentChunk", back_populates="document")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    chunk_order = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    chunk_metadata = Column(JSON)  # Additional metadata for the chunk
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to document
    document = relationship("Document", back_populates="chunks")

    # Relationship to chunk mappings
    mappings = relationship("ChunkMapping", back_populates="chunk")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Allow NULL for anonymous sessions
    session_title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"))
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    context_used = Column(JSON)  # IDs of document chunks used for response
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship back to session
    session = relationship("ChatSession", back_populates="messages")


class ChunkMapping(Base):
    __tablename__ = "chunk_mappings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chunk_id = Column(UUID(as_uuid=True), ForeignKey("document_chunks.id"))
    qdrant_point_id = Column(String(255), nullable=False)  # Point ID in Qdrant
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to chunk
    chunk = relationship("DocumentChunk", back_populates="mappings")