from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any
from app.models.message import MessageRoleEnum


class Citation(BaseModel):
    subset: str
    section: Optional[str] = None
    paragraph: Optional[str] = None
    page: Optional[int] = None
    line: Optional[int] = None
    text: str
    document_id: str


class MessageBase(BaseModel):
    role: MessageRoleEnum
    content: str


class MessageCreate(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    style: str = "professional"


class MessageResponse(MessageBase):
    id: str
    conversation_id: str
    citations: List[Citation] = []
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    conversation_id: str
    message: MessageResponse
    citations: List[Citation] = []
