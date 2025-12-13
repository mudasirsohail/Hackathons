from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.db import get_db
from ..models.request_models import (
    DocumentCreate,
    DocumentIngestResponse,
    IngestDocumentsRequest,
    BulkIngestResponse,
    QueryRequest,
    QueryResponse
)
from ..services.document_service import DocumentService
from ..vector_store.qdrant_client import QdrantWrapper
from ..services.embedding_service import EmbeddingService
from ..utils.loader import load_docusaurus_docs
from ..utils.logger import logger


router = APIRouter(prefix="/ingest", tags=["ingestion"])


@router.post("/documents", response_model=List[DocumentIngestResponse])
def ingest_documents(request: IngestDocumentsRequest, db: Session = Depends(get_db)):
    """
    Ingest multiple documents into the system
    """
    try:
        qdrant_wrapper = QdrantWrapper()
        embedding_service = EmbeddingService()
        document_service = DocumentService(db, qdrant_wrapper, embedding_service)
        
        # Process each document
        results = []
        for doc_data in request.documents:
            result = document_service.ingest_document(doc_data.dict())
            results.append(DocumentIngestResponse(**result))
        
        return results
    
    except Exception as e:
        logger.error(f"Error ingesting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/docusaurus", response_model=BulkIngestResponse)
def ingest_docusaurus_docs(docs_dir: str, db: Session = Depends(get_db)):
    """
    Ingest all Docusaurus docs from a directory
    """
    try:
        # Load documents from the Docusaurus directory
        import asyncio
        docs_data = asyncio.run(load_docusaurus_docs(docs_dir))
        
        qdrant_wrapper = QdrantWrapper()
        embedding_service = EmbeddingService()
        document_service = DocumentService(db, qdrant_wrapper, embedding_service)
        
        # Process each document
        results = []
        for doc_data in docs_data:
            doc_dict = {
                'title': doc_data['title'],
                'source_path': doc_data['source_path'],
                'content': doc_data['content'],
                'checksum': str(doc_data['checksum'])
            }
            
            try:
                result = document_service.ingest_document(doc_dict)
                results.append(DocumentIngestResponse(**result))
            except Exception as e:
                logger.error(f"Failed to ingest document {doc_data['title']}: {str(e)}")
                results.append(DocumentIngestResponse(
                    document_id="",
                    status="error",
                    message=f"Failed to ingest: {str(e)}"
                ))
        
        return BulkIngestResponse(results=results)
    
    except Exception as e:
        logger.error(f"Error ingesting Docusaurus docs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Query documents using semantic search
    """
    try:
        qdrant_wrapper = QdrantWrapper()
        embedding_service = EmbeddingService()
        
        # Embed the query
        query_embedding = embedding_service.embed_text(request.query)
        
        # Search in Qdrant
        results = qdrant_wrapper.search_similar(query_embedding, top_k=request.top_k)
        
        return QueryResponse(results=results)
    
    except Exception as e:
        logger.error(f"Error querying documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))