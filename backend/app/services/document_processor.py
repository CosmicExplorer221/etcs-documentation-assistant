"""
Document Processing Service - Extracts text from PDFs and creates chunks
"""

import fitz  # PyMuPDF
import re
from typing import List, Dict, Tuple
from pathlib import Path
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class DocumentChunk:
    """Represents a chunk of text from a document"""

    def __init__(
        self,
        text: str,
        document_id: str,
        subset: str,
        page: int,
        chunk_index: int,
        section: str = None,
        paragraph: int = None
    ):
        self.text = text
        self.document_id = document_id
        self.subset = subset
        self.page = page
        self.chunk_index = chunk_index
        self.section = section
        # Convert paragraph to string if it's an integer
        self.paragraph = str(paragraph) if paragraph is not None else None

    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            "text": self.text,
            "document_id": self.document_id,
            "subset": self.subset,
            "page": self.page,
            "chunk_index": self.chunk_index,
            "section": self.section,
            "paragraph": self.paragraph
        }


class DocumentProcessor:
    """Process PDF documents and extract text with metadata"""

    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

    def extract_text_from_pdf(self, pdf_path: str) -> List[Tuple[int, str]]:
        """
        Extract text from PDF file

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of tuples (page_number, page_text)
        """
        try:
            doc = fitz.open(pdf_path)
            pages_text = []

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()

                # Clean up text
                text = self._clean_text(text)

                pages_text.append((page_num + 1, text))  # 1-indexed pages

            doc.close()
            logger.info(f"Extracted text from {len(pages_text)} pages from {pdf_path}")
            return pages_text

        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            raise

    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove page numbers and headers/footers (common patterns)
        text = re.sub(r'Page \d+', '', text)
        text = re.sub(r'\d+\s+of\s+\d+', '', text)

        # Remove special characters that may cause issues
        text = text.replace('\x00', '')

        return text.strip()

    def create_chunks(
        self,
        pages_text: List[Tuple[int, str]],
        document_id: str,
        subset: str
    ) -> List[DocumentChunk]:
        """
        Create overlapping chunks from page text

        Args:
            pages_text: List of (page_number, text) tuples
            document_id: Unique identifier for the document
            subset: Subset number (e.g., "Subset-026")

        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        chunk_index = 0

        for page_num, page_text in pages_text:
            # Split page into paragraphs
            paragraphs = self._split_into_paragraphs(page_text)

            current_chunk = ""
            current_paragraph = 0

            for para_idx, paragraph in enumerate(paragraphs):
                # If adding this paragraph would exceed chunk size
                if len(current_chunk) + len(paragraph) > self.chunk_size and current_chunk:
                    # Save current chunk
                    section = self._extract_section_number(current_chunk)

                    chunk = DocumentChunk(
                        text=current_chunk,
                        document_id=document_id,
                        subset=subset,
                        page=page_num,
                        chunk_index=chunk_index,
                        section=section,
                        paragraph=current_paragraph
                    )
                    chunks.append(chunk)
                    chunk_index += 1

                    # Start new chunk with overlap
                    overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else current_chunk
                    current_chunk = overlap_text + " " + paragraph
                    current_paragraph = para_idx
                else:
                    # Add paragraph to current chunk
                    if current_chunk:
                        current_chunk += " " + paragraph
                    else:
                        current_chunk = paragraph
                    current_paragraph = para_idx

            # Add remaining chunk from this page
            if current_chunk:
                section = self._extract_section_number(current_chunk)
                chunk = DocumentChunk(
                    text=current_chunk,
                    document_id=document_id,
                    subset=subset,
                    page=page_num,
                    chunk_index=chunk_index,
                    section=section,
                    paragraph=current_paragraph
                )
                chunks.append(chunk)
                chunk_index += 1

        logger.info(f"Created {len(chunks)} chunks from {len(pages_text)} pages")
        return chunks

    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        # Split on double newlines or periods followed by newline
        paragraphs = re.split(r'\n\n+|\.\s*\n', text)

        # Filter out empty paragraphs and very short ones
        paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 50]

        return paragraphs

    def _extract_section_number(self, text: str) -> str:
        """
        Extract section number from text (e.g., "3.4.2", "§3.4.2")

        Args:
            text: Text to search for section number

        Returns:
            Section number or None
        """
        # Look for patterns like "3.4.2" or "§3.4.2" or "Section 3.4.2"
        patterns = [
            r'§\s*(\d+(?:\.\d+)*)',  # §3.4.2
            r'Section\s+(\d+(?:\.\d+)*)',  # Section 3.4.2
            r'(\d+\.\d+(?:\.\d+)*)',  # 3.4.2 (at least two levels)
        ]

        for pattern in patterns:
            match = re.search(pattern, text[:200])  # Search in first 200 chars
            if match:
                return match.group(1)

        return None

    def process_document(
        self,
        pdf_path: str,
        document_id: str,
        subset: str
    ) -> List[DocumentChunk]:
        """
        Process a PDF document: extract text and create chunks

        Args:
            pdf_path: Path to PDF file
            document_id: Unique identifier for document
            subset: Subset number (e.g., "Subset-026")

        Returns:
            List of DocumentChunk objects
        """
        logger.info(f"Processing document: {pdf_path}")

        # Extract text from PDF
        pages_text = self.extract_text_from_pdf(pdf_path)

        # Create chunks
        chunks = self.create_chunks(pages_text, document_id, subset)

        logger.info(f"Successfully processed document: {len(chunks)} chunks created")
        return chunks


# Global instance
document_processor = DocumentProcessor()
