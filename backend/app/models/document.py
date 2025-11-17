from sqlalchemy import Column, String, DateTime, Integer, Boolean, Text
from datetime import datetime
import uuid
from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    subset_number = Column(String, nullable=False, index=True)  # e.g., "Subset-026"
    version = Column(String, nullable=False)  # e.g., "4.0.0"
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)  # in bytes
    page_count = Column(Integer)
    description = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)  # Whether document has been indexed
    processed_at = Column(DateTime, nullable=True)

    # Metadata
    upload_user_id = Column(String, nullable=True)  # Track who uploaded
