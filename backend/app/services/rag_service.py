"""
RAG (Retrieval-Augmented Generation) Service
Orchestrates document search and AI response generation
"""

import re
from typing import List, Dict, Optional
import logging
from app.services.vector_store import vector_store
from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)


class RAGService:
    """Service for performing RAG (Retrieval-Augmented Generation)"""

    def __init__(self):
        self.vector_store = vector_store
        self.gemini_service = gemini_service

    def search_documents(
        self,
        query: str,
        top_k: int = 5,
        subset_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for relevant document chunks

        Args:
            query: User's search query
            top_k: Number of results to return
            subset_filter: Optional filter by subset

        Returns:
            List of relevant document chunks with metadata
        """
        try:
            # Generate embedding for query
            query_embedding = self.gemini_service.generate_embedding(query)

            # Search vector store
            results = self.vector_store.search(
                query_embedding=query_embedding,
                top_k=top_k,
                subset_filter=subset_filter
            )

            return results

        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            raise

    def generate_response(
        self,
        query: str,
        style: str = "professional",
        subset_filter: Optional[str] = None,
        top_k: int = 5
    ) -> Dict:
        """
        Generate AI response using RAG

        Args:
            query: User's question
            style: Conversation style
            subset_filter: Optional filter by subset
            top_k: Number of context chunks to retrieve

        Returns:
            Dictionary with response and citations
        """
        try:
            # Search for relevant documents
            search_results = self.search_documents(
                query=query,
                top_k=top_k,
                subset_filter=subset_filter
            )

            if not search_results:
                return {
                    "response": "I couldn't find relevant information in the ETCS documentation to answer your question. Please try rephrasing or ask about a different topic.",
                    "citations": [],
                    "context_chunks": []
                }

            # Build context from search results
            context = self._build_context(search_results)

            # Generate AI response
            ai_response = self.gemini_service.generate_chat_response(
                prompt=query,
                context=context,
                style=style
            )

            # Extract citations from response
            citations = self._extract_citations(ai_response, search_results)

            return {
                "response": ai_response,
                "citations": citations,
                "context_chunks": search_results[:3],  # Include top 3 for debugging
            }

        except Exception as e:
            logger.error(f"Error generating RAG response: {e}")
            raise

    def _build_context(self, search_results: List[Dict]) -> str:
        """
        Build context string from search results

        Args:
            search_results: List of search results with text and metadata

        Returns:
            Formatted context string
        """
        context_parts = []

        for idx, result in enumerate(search_results, 1):
            # Format metadata
            metadata = f"[{result['subset']}"
            if result.get('section'):
                metadata += f", §{result['section']}"
            if result.get('page'):
                metadata += f", p.{result['page']}"
            if result.get('paragraph'):
                metadata += f", ¶{result['paragraph']}"
            metadata += "]"

            # Add to context
            context_parts.append(f"{metadata}\n{result['text']}\n")

        return "\n".join(context_parts)

    def _extract_citations(
        self,
        ai_response: str,
        search_results: List[Dict]
    ) -> List[Dict]:
        """
        Extract citations from AI response

        Args:
            ai_response: Generated AI response text
            search_results: Search results used for context

        Returns:
            List of citation objects
        """
        citations = []

        # Pattern to match citations like [Subset-026, §3.4.2, p.42, ¶5]
        citation_pattern = r'\[([^\]]+)\]'
        matches = re.findall(citation_pattern, ai_response)

        for match in matches:
            # Parse citation components
            parts = [p.strip() for p in match.split(',')]

            citation = {}

            for part in parts:
                # Subset
                if part.startswith('Subset-'):
                    citation['subset'] = part
                # Section
                elif part.startswith('§'):
                    citation['section'] = part[1:].strip()
                # Page
                elif part.startswith('p.'):
                    try:
                        citation['page'] = int(part[2:].strip())
                    except ValueError:
                        pass
                # Paragraph
                elif part.startswith('¶'):
                    citation['paragraph'] = part[1:].strip()

            # Find matching chunk for full text and document_id
            if citation.get('subset'):
                for result in search_results:
                    if result['subset'] == citation['subset']:
                        citation['text'] = result['text'][:200] + "..."  # First 200 chars
                        citation['document_id'] = result['document_id']
                        break

            # Only add if we have required fields
            if citation.get('text') and citation.get('document_id'):
                citations.append(citation)

        # If no citations found in text, create them from top results
        if not citations and search_results:
            for result in search_results[:3]:  # Top 3 results
                # Convert paragraph to string if it's an integer (for old data compatibility)
                paragraph = result.get('paragraph')
                if paragraph is not None and not isinstance(paragraph, str):
                    paragraph = str(paragraph)

                citation = {
                    'subset': result['subset'],
                    'section': result.get('section'),
                    'page': result.get('page'),
                    'paragraph': paragraph,
                    'text': result['text'][:200] + "...",
                    'document_id': result['document_id'],
                }
                citations.append(citation)

        return citations


# Global instance
rag_service = RAGService()
