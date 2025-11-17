"""
Qdrant Vector Store Service - Manages document embeddings and similarity search
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Optional
import logging
from app.core.config import settings
from app.services.document_processor import DocumentChunk

logger = logging.getLogger(__name__)


class VectorStore:
    """Service for managing document embeddings in Qdrant"""

    def __init__(self):
        # Initialize Qdrant client
        # Qdrant Cloud: use URL + API key
        # Local Docker: use localhost
        qdrant_url = settings.get_qdrant_url()

        if settings.QDRANT_API_KEY:
            # Qdrant Cloud with authentication
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=settings.QDRANT_API_KEY
            )
            logger.info(f"Connected to Qdrant Cloud: {qdrant_url}")
        else:
            # Local Docker or custom URL
            self.client = QdrantClient(url=qdrant_url)
            logger.info(f"Connected to local Qdrant: {qdrant_url}")

        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def create_collection(self, vector_size: int = 768):
        """
        Create Qdrant collection for storing document embeddings

        Args:
            vector_size: Size of embedding vectors (Gemini text-embedding-004 = 768)
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name in collection_names:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return

            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,  # Cosine similarity for embeddings
                ),
            )
            logger.info(f"Created collection '{self.collection_name}'")

        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise

    def add_documents(
        self,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]]
    ):
        """
        Add document chunks with embeddings to vector store

        Args:
            chunks: List of DocumentChunk objects
            embeddings: Corresponding embedding vectors
        """
        try:
            if len(chunks) != len(embeddings):
                raise ValueError("Number of chunks must match number of embeddings")

            # Prepare points for Qdrant
            points = []
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point = PointStruct(
                    id=idx,  # Simple sequential ID
                    vector=embedding,
                    payload={
                        "text": chunk.text,
                        "document_id": chunk.document_id,
                        "subset": chunk.subset,
                        "page": chunk.page,
                        "chunk_index": chunk.chunk_index,
                        "section": chunk.section,
                        "paragraph": chunk.paragraph,
                    }
                )
                points.append(point)

            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

            logger.info(f"Added {len(points)} document chunks to vector store")

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise

    def search(
        self,
        query_embedding: List[float],
        top_k: int = None,
        subset_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for similar documents using vector similarity

        Args:
            query_embedding: Embedding vector for the query
            top_k: Number of results to return
            subset_filter: Optional filter by subset (e.g., "Subset-026")

        Returns:
            List of search results with text and metadata
        """
        try:
            if top_k is None:
                top_k = settings.TOP_K_RESULTS

            # Build filter if subset specified
            search_filter = None
            if subset_filter:
                from qdrant_client.models import Filter, FieldCondition, MatchValue
                search_filter = Filter(
                    must=[
                        FieldCondition(
                            key="subset",
                            match=MatchValue(value=subset_filter)
                        )
                    ]
                )

            # Perform search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=search_filter,
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "text": result.payload["text"],
                    "document_id": result.payload["document_id"],
                    "subset": result.payload["subset"],
                    "page": result.payload["page"],
                    "chunk_index": result.payload["chunk_index"],
                    "section": result.payload.get("section"),
                    "paragraph": result.payload.get("paragraph"),
                    "score": result.score,  # Similarity score
                })

            logger.info(f"Found {len(formatted_results)} results for query")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            raise

    def get_collection_info(self) -> Dict:
        """Get information about the collection"""
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}

    def delete_collection(self):
        """Delete the collection (use with caution!)"""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info(f"Deleted collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise


# Global instance
vector_store = VectorStore()
