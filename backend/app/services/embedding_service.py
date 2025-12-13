from typing import List
import numpy as np
from ..config.settings import settings
from ..utils.logger import logger


class EmbeddingService:
    def __init__(self):
        # Initialize with a fixed dimension
        self.dimension = 384  # Standard for sentence transformers
        logger.info(f"Initialized mock embedding service with dimension {self.dimension}")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate a mock embedding for a single text
        Args:
            text: Input text to embed
        Returns:
            Mock embedding as a list of floats
        """
        # Create a mock embedding using simple hashing approach
        # This is just for demonstration - not an actual semantic embedding
        hash_input = text.encode('utf-8')
        hash_val = hash(text) % (2**32)
        
        # Set the seed to ensure consistent embeddings for the same text
        np.random.seed(abs(hash_val))
        
        # Generate a random vector with the required dimension
        embedding = np.random.random(self.dimension).tolist()
        
        return embedding

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate mock embeddings for multiple texts
        Args:
            texts: List of input texts to embed
        Returns:
            List of mock embeddings, each as a list of floats
        """
        return [self.embed_text(text) for text in texts]
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings
        """
        return self.dimension