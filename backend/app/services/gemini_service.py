"""
Gemini AI Service - Handles chat and embeddings using Google's Gemini API
"""

import google.generativeai as genai
from typing import List, Dict, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiService:
    """Service for interacting with Google Gemini API"""

    def __init__(self):
        self.chat_model = "gemini-pro"  # Stable model name
        self.embedding_model = "models/text-embedding-004"

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text using Gemini

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings

    def generate_chat_response(
        self,
        prompt: str,
        context: str,
        style: str = "professional",
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate chat response using Gemini

        Args:
            prompt: User's question
            context: Retrieved context from documents
            style: Conversation style
            conversation_history: Previous messages in conversation

        Returns:
            Generated response text
        """
        try:
            # Build system instruction based on style
            system_instruction = self._get_system_instruction(style)

            # Build full prompt with context
            full_prompt = f"""You are an ETCS (European Train Control System) expert assistant.

{system_instruction}

IMPORTANT: When referencing information from the context below, cite your sources using this format:
[Subset-XXX, §X.X.X, p.XX, ¶X]

For example: "The Movement Authority defines the distance..." [Subset-026, §3.4.2, p.42, ¶5]

Context from ETCS documentation:
{context}

User Question: {prompt}

Provide a detailed, accurate answer based on the context above. Include citations for all factual statements."""

            # Initialize model
            model = genai.GenerativeModel(
                model_name=self.chat_model,
                generation_config={
                    "temperature": 0.3,  # Lower for more factual responses
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )

            # Generate response
            response = model.generate_content(full_prompt)
            return response.text

        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            raise

    def _get_system_instruction(self, style: str) -> str:
        """Get system instruction based on conversation style"""

        style_instructions = {
            "professional": """
                You are speaking to experienced railway engineers. Use precise technical terminology,
                reference standards directly, and provide detailed explanations. Maintain a formal,
                professional tone suitable for technical documentation.
            """,
            "entry-level": """
                You are explaining ETCS to junior engineers with basic railway knowledge.
                Use clear language, define acronyms on first use, and provide context for technical terms.
                Break down complex concepts into understandable parts while maintaining accuracy.
            """,
            "newbie": """
                You are introducing ETCS concepts to someone new to railway systems.
                Use simple language and everyday analogies to explain concepts. Avoid jargon unless
                you define it first. Focus on fundamental understanding before technical details.
            """,
            "ten-year-old": """
                Explain ETCS concepts using very simple language that a 10-year-old could understand.
                Use fun analogies, comparisons to everyday things, and avoid technical jargon.
                Make it engaging and easy to grasp.
            """,
            "detailed": """
                Provide in-depth, comprehensive technical explanations. Include all relevant details,
                specifications, edge cases, and technical nuances. Reference multiple sections of
                documentation when relevant. Assume high technical competence.
            """,
            "concise": """
                Provide brief, to-the-point answers. Focus on key information only.
                Use bullet points where appropriate. Avoid unnecessary elaboration while
                maintaining accuracy.
            """,
            "funny": """
                Explain ETCS concepts with humor and wit, while maintaining technical accuracy.
                Use clever analogies, light jokes, and an engaging tone. Keep it professional
                but entertaining. Technical accuracy is still paramount.
            """,
            "academic": """
                Use formal, research-oriented language suitable for academic papers or technical
                publications. Reference standards formally, discuss methodologies, and present
                information with scholarly rigor.
            """,
            "practical": """
                Focus on real-world application and implementation. Explain how concepts work
                in practice, common challenges, and practical considerations. Include examples
                from actual railway operations where relevant.
            """
        }

        return style_instructions.get(style, style_instructions["professional"])


# Global instance
gemini_service = GeminiService()
