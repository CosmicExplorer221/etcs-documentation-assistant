from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from app.core.database import get_db
from app.models import Conversation, Message, MessageRoleEnum
from app.schemas.conversation import ConversationResponse, ConversationWithMessages
from app.schemas.message import MessageCreate, MessageResponse, ChatResponse
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# Demo mode - single user ID for all requests
DEMO_USER_ID = "demo-user"


@router.post("/message", response_model=ChatResponse)
async def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
):
    """Send a message and get AI response"""
    conversation = None

    # If conversation_id is provided, verify it exists
    if message_data.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == message_data.conversation_id,
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=DEMO_USER_ID,
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

    # Generate AI response using RAG (Phase 2)
    try:
        rag_result = rag_service.generate_response(
            query=message_data.message,
            style=message_data.style,
            subset_filter=None,  # Can be extended to allow filtering
            top_k=5
        )

        ai_response_content = rag_result["response"]
        citations = rag_result["citations"]

        logger.info(f"Generated RAG response with {len(citations)} citations")

    except Exception as e:
        logger.error(f"Error generating RAG response: {e}")
        # Fallback to simple error message
        ai_response_content = (
            "I apologize, but I encountered an error while searching the ETCS documentation. "
            "Please ensure the documents are properly loaded and try again."
        )
        citations = []

    # Save assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role=MessageRoleEnum.ASSISTANT,
        content=ai_response_content,
        citations=citations,
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return ChatResponse(
        conversation_id=conversation.id,
        message=MessageResponse.model_validate(assistant_message),
        citations=citations,
    )


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    db: Session = Depends(get_db),
):
    """Get all conversations (demo mode - all conversations)"""
    conversations = (
        db.query(Conversation)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    return [ConversationResponse.model_validate(conv) for conv in conversations]


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific conversation with all messages"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
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
    db: Session = Depends(get_db),
):
    """Delete a conversation"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    db.delete(conversation)
    db.commit()

    return None
