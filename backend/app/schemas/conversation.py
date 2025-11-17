from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.conversation import ConversationStyleEnum


class ConversationBase(BaseModel):
    title: str
    style: ConversationStyleEnum


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"
    style: ConversationStyleEnum = ConversationStyleEnum.PROFESSIONAL


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    style: Optional[ConversationStyleEnum] = None


class ConversationResponse(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# For responses that include messages
class ConversationWithMessages(ConversationResponse):
    messages: List["MessageResponse"] = []


# Import at the end to avoid circular imports
from app.schemas.message import MessageResponse
ConversationWithMessages.model_rebuild()
