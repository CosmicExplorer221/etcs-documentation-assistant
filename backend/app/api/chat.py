from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models import Conversation, Message, MessageRoleEnum
from app.schemas.conversation import ConversationResponse, ConversationWithMessages
from app.schemas.message import MessageCreate, MessageResponse, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=ChatResponse)
async def send_message(
    message_data: MessageCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Send a message and get AI response"""
    conversation = None

    # If conversation_id is provided, verify it exists and belongs to user
    if message_data.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == message_data.conversation_id,
            Conversation.user_id == user_id,
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=user_id,
            title=message_data.message[:50] + "..." if len(message_data.message) > 50 else message_data.message,
            style=message_data.style,
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role=MessageRoleEnum.USER,
        content=message_data.message,
    )
    db.add(user_message)
    db.commit()

    # TODO: Phase 2 - Call RAG system to generate AI response
    # For now, return a placeholder response
    ai_response_content = (
        f"This is a placeholder response in {message_data.style} style. "
        "The actual RAG system will be integrated in Phase 2 with real ETCS documentation."
    )

    # Mock citations for demonstration
    mock_citations = [
        {
            "subset": "Subset-026",
            "section": "3.4.2",
            "page": 42,
            "paragraph": "5",
            "text": "Example citation text from the document",
            "document_id": "doc-placeholder",
        }
    ]

    # Save assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role=MessageRoleEnum.ASSISTANT,
        content=ai_response_content,
        citations=mock_citations,
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return ChatResponse(
        conversation_id=conversation.id,
        message=MessageResponse.model_validate(assistant_message),
        citations=mock_citations,
    )


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Get all conversations for the current user"""
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    return [ConversationResponse.model_validate(conv) for conv in conversations]


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Get a specific conversation with all messages"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return ConversationWithMessages.model_validate(conversation)


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Delete a conversation"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    db.delete(conversation)
    db.commit()

    return None
