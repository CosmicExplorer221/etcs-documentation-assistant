from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.core.database import Base


class ConversationStyleEnum(str, enum.Enum):
    PROFESSIONAL = "professional"
    ENTRY_LEVEL = "entry-level"
    NEWBIE = "newbie"
    TEN_YEAR_OLD = "ten-year-old"
    DETAILED = "detailed"
    CONCISE = "concise"
    FUNNY = "funny"
    ACADEMIC = "academic"
    PRACTICAL = "practical"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False, default="New Conversation")
    style = Column(Enum(ConversationStyleEnum), default=ConversationStyleEnum.PROFESSIONAL)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="conversation", cascade="all, delete-orphan")
