from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.core.database import Base


class MessageRoleEnum(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(MessageRoleEnum), nullable=False)
    content = Column(Text, nullable=False)
    citations = Column(JSON, default=list)  # Store citation data as JSON
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    bookmarks = relationship("Bookmark", back_populates="message", cascade="all, delete-orphan")
