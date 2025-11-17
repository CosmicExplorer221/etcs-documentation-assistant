"""
Documents API - Manage ETCS documentation
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
import logging
from pydantic import BaseModel
from app.core.config import settings
from app.services.document_processor import document_processor
from app.services.gemini_service import gemini_service
from app.services.vector_store import vector_store
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])


# Pydantic models
class DocumentInfo(BaseModel):
    """Document information"""
    filename: str
    subset: str
    path: str
    processed: bool


class SearchRequest(BaseModel):
    """Search request"""
    query: str
    top_k: int = 5
    subset_filter: str = None


class SearchResult(BaseModel):
    """Search result"""
    text: str
    subset: str
    page: int
    section: str = None
    score: float


@router.get("/list", response_model=List[DocumentInfo])
async def list_documents():
    """
    List all available ETCS documents

    Returns:
        List of documents with metadata
    """
    try:
        documents_dir = Path(settings.DOCUMENTS_DIR)

        if not documents_dir.exists():
            return []

        documents = []
        for pdf_file in documents_dir.glob("*.pdf"):
            # Extract subset from filename (e.g., "Subset-026.pdf" -> "Subset-026")
            subset = pdf_file.stem

            documents.append(DocumentInfo(
                filename=pdf_file.name,
                subset=subset,
                path=str(pdf_file),
                processed=False,  # TODO: Track processing status in database
            ))

        return documents

    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_collection_info():
    """
    Get information about the vector store collection

    Returns:
        Collection statistics
    """
    try:
        info = vector_store.get_collection_info()
        return info
    except Exception as e:
        logger.error(f"Error getting collection info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[SearchResult])
async def search_documents(search_request: SearchRequest):
    """
    Search for documents using semantic search

    Args:
        search_request: Search parameters

    Returns:
        List of relevant document chunks
    """
    try:
        results = rag_service.search_documents(
            query=search_request.query,
            top_k=search_request.top_k,
            subset_filter=search_request.subset_filter
        )

        # Convert to response model
        search_results = []
        for result in results:
            search_results.append(SearchResult(
                text=result['text'],
                subset=result['subset'],
                page=result['page'],
                section=result.get('section'),
                score=result['score']
            ))

        return search_results

    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pdf/{filename}")
async def get_pdf(filename: str):
    """
    Serve a PDF file for viewing

    Args:
        filename: Name of the PDF file

    Returns:
        PDF file
    """
    try:
        documents_dir = Path(settings.DOCUMENTS_DIR)
        pdf_path = documents_dir / filename

        # Security check: ensure file is within documents directory
        if not pdf_path.resolve().is_relative_to(documents_dir.resolve()):
            raise HTTPException(status_code=403, detail="Access denied")

        if not pdf_path.exists():
            raise HTTPException(status_code=404, detail="Document not found")

        if not pdf_path.suffix.lower() == '.pdf':
            raise HTTPException(status_code=400, detail="File is not a PDF")

        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=filename
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))
