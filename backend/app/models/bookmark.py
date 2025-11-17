from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    message_id = Column(String, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="bookmarks")
    conversation = relationship("Conversation", back_populates="bookmarks")
    message = relationship("Message", back_populates="bookmarks")
