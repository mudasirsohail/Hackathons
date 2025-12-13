from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..database.schemas import Document, DocumentChunk, ChunkMapping
from ..vector_store.qdrant_client import QdrantWrapper
from ..services.embedding_service import EmbeddingService
from ..utils.chunker import chunk_document
from ..utils.logger import logger


class DocumentService:
    def __init__(self, db: Session, qdrant_wrapper: QdrantWrapper, embedding_service: EmbeddingService):
        self.db = db
        self.qdrant = qdrant_wrapper
        self.embedding_service = embedding_service

    def ingest_document(self, doc_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingest a document into the system
        Args:
            doc_data: Dictionary containing document information
        Returns:
            Dictionary with ingestion results
        """
        try:
            # Check if document with same checksum already exists
            existing_doc = self.db.query(Document).filter(
                Document.checksum == doc_data['checksum']
            ).first()
            
            if existing_doc:
                # Document already exists, return existing ID
                return {
                    'document_id': str(existing_doc.id),
                    'status': 'already_exists',
                    'message': 'Document already exists in the database'
                }
            
            # Create new document record
            document = Document(
                title=doc_data['title'],
                source_path=doc_data['source_path'],
                checksum=doc_data['checksum'],
                doc_metadata={'original_length': len(doc_data['content'])}
            )
            
            self.db.add(document)
            self.db.commit()
            self.db.refresh(document)
            
            # Chunk the document content
            chunked_docs = chunk_document({
                'id': document.id,
                'content': doc_data['content'],
                'source_path': doc_data['source_path'],
                'title': doc_data['title']
            })
            
            # Process each chunk
            all_text_embeddings_pairs = []
            chunk_records = []
            
            for chunk_doc in chunked_docs:
                # Create document chunk record
                chunk_record = DocumentChunk(
                    document_id=document.id,
                    chunk_order=chunk_doc['chunk_order'],
                    content=chunk_doc['content'],
                    chunk_metadata=chunk_doc['embedding_metadata']
                )
                
                self.db.add(chunk_record)
                chunk_records.append(chunk_record)
            
            self.db.commit()
            
            # Get embeddings for all chunks
            texts = [chunk.content for chunk in chunk_records]
            embeddings = self.embedding_service.embed_texts(texts)

            # Store embeddings in Qdrant
            metadata_list = [
                {
                    'document_id': str(chunk.document_id),
                    'chunk_order': chunk.chunk_order,
                    'source_path': chunk.chunk_metadata['source']
                }
                for chunk in chunk_records
            ]

            qdrant_ids = self.qdrant.store_embeddings(texts, embeddings, metadata_list)
            
            # Create mapping records
            for chunk, qdrant_id in zip(chunk_records, qdrant_ids):
                mapping = ChunkMapping(
                    chunk_id=chunk.id,
                    qdrant_point_id=qdrant_id
                )
                self.db.add(mapping)
            
            self.db.commit()
            
            logger.info(f"Ingested document '{document.title}' with {len(chunk_records)} chunks")
            
            return {
                'document_id': str(document.id),
                'status': 'success',
                'chunks_created': len(chunk_records),
                'message': f'Successfully ingested document with {len(chunk_records)} chunks'
            }
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error ingesting document: {str(e)}")
            raise

    def ingest_documents_bulk(self, docs_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Bulk ingest multiple documents
        Args:
            docs_data: List of document data dictionaries
        Returns:
            List of ingestion results for each document
        """
        results = []
        
        for doc_data in docs_data:
            try:
                result = self.ingest_document(doc_data)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to ingest document {doc_data.get('title', 'Unknown')}: {str(e)}")
                results.append({
                    'document_title': doc_data.get('title', 'Unknown'),
                    'status': 'error',
                    'error': str(e)
                })
        
        return results