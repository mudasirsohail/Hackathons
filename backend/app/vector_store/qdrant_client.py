from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any
from uuid import uuid4
from ..config.settings import settings
from ..utils.logger import logger


class QdrantWrapper:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=True
        )
        self.collection_name = settings.DOCUMENT_COLLECTION_NAME

        # Initialize the collection if it doesn't exist
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection if it doesn't exist"""
        try:
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name not in collection_names:
                # We'll determine the vector size when we create the first collection
                # It will be based on the embedding model used
                vector_size = 384  # Default for all-MiniLM-L6-v2 model

                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection {self.collection_name} already exists")

        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {str(e)}")
            raise

    def store_embeddings(self, texts: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]], ids: List[str] = None) -> List[str]:
        """
        Store text embeddings in Qdrant
        Args:
            texts: List of text strings to store
            embeddings: List of embedding vectors corresponding to each text
            metadatas: List of metadata dicts corresponding to each text
            ids: Optional list of IDs for the points (if not provided, random IDs will be generated)
        Returns:
            List of point IDs that were stored
        """
        try:
            if ids is None:
                ids = [str(uuid4()) for _ in texts]

            # Prepare the points to insert
            points = [
                PointStruct(
                    id=id_,
                    vector=embedding,
                    payload={
                        "text": text,
                        "metadata": metadata
                    }
                )
                for id_, text, embedding, metadata in zip(ids, texts, embeddings, metadatas)
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Stored {len(texts)} embeddings in Qdrant collection: {self.collection_name}")
            return ids

        except Exception as e:
            logger.error(f"Error storing embeddings in Qdrant: {str(e)}")
            raise

    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant
        Args:
            query_embedding: The embedding vector to search for
            top_k: Number of top similar results to return
        Returns:
            List of similar results with text and metadata
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )

            # Format results to return text and metadata
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'id': result.id,
                    'text': result.payload.get('text', ''),
                    'metadata': result.payload.get('metadata', {}),
                    'score': result.score
                })

            logger.info(f"Found {len(formatted_results)} similar results in Qdrant")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching in Qdrant: {str(e)}")
            raise

    def delete_points(self, point_ids: List[str]):
        """
        Delete specific points from the collection
        Args:
            point_ids: List of point IDs to delete
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=point_ids
            )
            logger.info(f"Deleted {len(point_ids)} points from Qdrant collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting points from Qdrant: {str(e)}")
            raise