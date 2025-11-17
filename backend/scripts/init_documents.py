#!/usr/bin/env python3
"""
Document Initialization Script
Processes all ETCS PDFs and loads them into the vector database
"""

import sys
import os
from pathlib import Path
import logging

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.services.document_processor import document_processor
from app.services.gemini_service import gemini_service
from app.services.vector_store import vector_store

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_documents():
    """
    Process all ETCS PDF documents and load them into Qdrant

    Steps:
    1. Find all PDFs in documents directory
    2. Extract text and create chunks
    3. Generate embeddings for chunks
    4. Store in Qdrant vector database
    """
    logger.info("=" * 60)
    logger.info("ETCS Document Initialization")
    logger.info("=" * 60)

    # Check if Gemini API key is set
    if not settings.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set! Please set it in .env file")
        logger.error("Get your free API key at: https://makersuite.google.com/app/apikey")
        return False

    # Check documents directory
    documents_dir = Path(settings.DOCUMENTS_DIR)
    if not documents_dir.exists():
        logger.error(f"Documents directory not found: {documents_dir}")
        logger.info(f"Please create directory and add ETCS PDF files")
        return False

    # Find all PDF files
    pdf_files = list(documents_dir.glob("*.pdf"))
    if not pdf_files:
        logger.warning(f"No PDF files found in {documents_dir}")
        return False

    logger.info(f"Found {len(pdf_files)} PDF files to process")

    # Create Qdrant collection
    logger.info("Creating Qdrant collection...")
    try:
        vector_store.create_collection(vector_size=768)  # Gemini embedding size
        logger.info("✓ Collection ready")
    except Exception as e:
        logger.error(f"Error creating collection: {e}")
        return False

    # Process each document
    total_chunks = 0
    successful_docs = 0

    for pdf_file in pdf_files:
        logger.info("-" * 60)
        logger.info(f"Processing: {pdf_file.name}")

        try:
            # Extract subset name from filename
            subset = pdf_file.stem  # e.g., "Subset-026"
            document_id = f"doc-{subset.lower()}"

            # Process PDF
            logger.info(f"  Extracting text from PDF...")
            chunks = document_processor.process_document(
                pdf_path=str(pdf_file),
                document_id=document_id,
                subset=subset
            )

            if not chunks:
                logger.warning(f"  No chunks extracted from {pdf_file.name}")
                continue

            logger.info(f"  ✓ Created {len(chunks)} chunks")

            # Generate embeddings
            logger.info(f"  Generating embeddings (this may take a while)...")
            chunk_texts = [chunk.text for chunk in chunks]

            embeddings = []
            for idx, text in enumerate(chunk_texts):
                if idx % 10 == 0:  # Progress update every 10 chunks
                    logger.info(f"    Progress: {idx}/{len(chunk_texts)} chunks")

                embedding = gemini_service.generate_embedding(text)
                embeddings.append(embedding)

            logger.info(f"  ✓ Generated {len(embeddings)} embeddings")

            # Store in vector database
            logger.info(f"  Storing in vector database...")
            vector_store.add_documents(chunks, embeddings)
            logger.info(f"  ✓ Stored in Qdrant")

            total_chunks += len(chunks)
            successful_docs += 1

        except Exception as e:
            logger.error(f"  ✗ Error processing {pdf_file.name}: {e}")
            continue

    # Summary
    logger.info("=" * 60)
    logger.info("Initialization Complete!")
    logger.info(f"  Processed: {successful_docs}/{len(pdf_files)} documents")
    logger.info(f"  Total chunks: {total_chunks}")
    logger.info("=" * 60)

    # Get collection info
    try:
        info = vector_store.get_collection_info()
        logger.info(f"Collection stats: {info}")
    except Exception as e:
        logger.warning(f"Could not get collection info: {e}")

    return successful_docs > 0


if __name__ == "__main__":
    logger.info("Starting document initialization...")

    success = initialize_documents()

    if success:
        logger.info("\n✓ Documents initialized successfully!")
        logger.info("You can now start the FastAPI server and test the RAG system")
        sys.exit(0)
    else:
        logger.error("\n✗ Document initialization failed")
        logger.error("Please check the errors above and try again")
        sys.exit(1)
