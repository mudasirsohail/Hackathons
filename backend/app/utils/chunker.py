from typing import List, Dict, Any
from .cleaner import preprocess_document
from .logger import logger


def chunk_text(content: str, chunk_size: int = 600, chunk_overlap: int = 50) -> List[str]:
    """
    Split text into chunks of specified size with overlap using simple Python methods
    """
    # Preprocess the document
    processed_content = preprocess_document(content)
    
    # Split content into sentences first
    sentences = processed_content.split('. ')
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # If adding this sentence would exceed the chunk size
        if len(current_chunk) + len(sentence) > chunk_size:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            
            # Start a new chunk, keeping some overlap if possible
            if len(sentence) > chunk_size:
                # If the sentence itself is longer than the chunk size, split it
                while len(sentence) > chunk_size:
                    chunks.append(sentence[:chunk_size])
                    sentence = sentence[chunk_size-chunk_overlap:]
                current_chunk = sentence
            else:
                current_chunk = sentence
        else:
            current_chunk += ". " + sentence if current_chunk else sentence
    
    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    # Log the number of chunks created
    logger.info(f"Text split into {len(chunks)} chunks")
    
    return chunks


def chunk_document(document: Dict[str, Any], chunk_size: int = 600, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Chunk a single document into multiple chunks with metadata
    """
    content = document['content']
    chunks = chunk_text(content, chunk_size, chunk_overlap)
    
    chunked_docs = []
    for i, chunk in enumerate(chunks):
        chunk_doc = {
            'document_id': document.get('id'),  # Will be added later when document is stored
            'chunk_order': i,
            'content': chunk,
            'source_path': document['source_path'],
            'title': document['title'],
            'embedding_metadata': {
                'source': document['source_path'],
                'title': document['title'],
                'chunk_order': i
            }
        }
        chunked_docs.append(chunk_doc)
    
    logger.info(f"Document '{document['title']}' split into {len(chunked_docs)} chunks")
    
    return chunked_docs