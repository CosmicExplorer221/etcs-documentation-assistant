"""
Simplified FastAPI Backend for Demo
No database required - uses in-memory storage
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

# Create FastAPI app
app = FastAPI(
    title="ETCS Documentation Assistant",
    version="0.1.0-demo",
    description="AI-powered ETCS documentation assistant (Demo Mode - In-Memory Storage)",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
conversations = {}
messages = {}

# Pydantic models
class MessageCreate(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    style: str = "professional"

class Citation(BaseModel):
    subset: str
    section: Optional[str] = None
    paragraph: Optional[str] = None
    page: Optional[int] = None
    line: Optional[int] = None
    text: str
    document_id: str

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    citations: List[Citation] = []
    created_at: str

class ChatResponse(BaseModel):
    conversation_id: str
    message: MessageResponse
    citations: List[Citation] = []

class ConversationResponse(BaseModel):
    id: str
    title: str
    style: str
    created_at: str
    updated_at: str

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "ETCS Documentation Assistant",
        "version": "0.1.0-demo",
        "status": "running",
        "mode": "demo - in-memory storage"
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Chat endpoint
@app.post("/api/v1/chat/message", response_model=ChatResponse)
async def send_message(message_data: MessageCreate):
    """Send a message and get AI response (demo mode)"""

    conversation_id = message_data.conversation_id

    # Create new conversation if needed
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        conversations[conversation_id] = {
            "id": conversation_id,
            "title": message_data.message[:50] + "..." if len(message_data.message) > 50 else message_data.message,
            "style": message_data.style,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        messages[conversation_id] = []

    # Check conversation exists
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Save user message
    user_message = {
        "id": str(uuid.uuid4()),
        "conversation_id": conversation_id,
        "role": "user",
        "content": message_data.message,
        "citations": [],
        "created_at": datetime.utcnow().isoformat(),
    }
    messages[conversation_id].append(user_message)

    # Generate AI response (placeholder)
    style_responses = {
        "professional": "This is a professional response about ETCS systems. The European Train Control System (ETCS) is a signalling, control and train protection system designed to replace the many incompatible safety systems currently used by European railways.",
        "entry-level": "Let me explain ETCS in simple terms. ETCS is a modern train control system that helps trains run safely across different European countries. It's like a universal language for trains!",
        "newbie": "ETCS is basically a safety system for trains. Think of it as helping trains know where they can go and how fast they can travel. It makes train travel safer!",
        "ten-year-old": "Imagine ETCS as a super smart helper for train drivers! It tells them when to speed up, slow down, or stop - kind of like a video game that keeps trains safe!",
        "detailed": "The European Train Control System (ETCS) comprises multiple operational levels (Level 0, 1, 2, and 3), each providing different degrees of train protection and control. Level 2, for instance, utilizes continuous radio communication between the train and Radio Block Centre (RBC)...",
        "concise": "ETCS: EU train control system. Ensures interoperability and safety across European railways.",
        "funny": "ETCS is like GPS for trains, but way cooler and it actually keeps trains from bumping into each other! No more 'Oops, wrong track!' moments. 🚂",
        "academic": "The European Train Control System represents a paradigm shift in railway signalling methodology, employing sophisticated algorithmic approaches to ensure operational safety and cross-border interoperability within the trans-European rail network.",
        "practical": "In practice, ETCS installations require careful coordination between infrastructure managers and train operators. Key implementation steps include: trackside equipment deployment, onboard unit installation, and comprehensive testing protocols.",
    }

    ai_content = style_responses.get(
        message_data.style,
        "This is a placeholder response. The RAG system with real ETCS documentation will be integrated in Phase 2."
    )

    # Mock citations
    mock_citations = [
        {
            "subset": "Subset-026",
            "section": "3.4.2",
            "page": 42,
            "paragraph": "5",
            "text": "The onboard equipment shall establish communication with the Radio Block Centre...",
            "document_id": "doc-subset-026",
        },
        {
            "subset": "Subset-037",
            "section": "2.1.3",
            "page": 18,
            "paragraph": "2",
            "text": "EuroRadio protocol ensures reliable data transmission between train and trackside...",
            "document_id": "doc-subset-037",
        }
    ]

    # Save assistant message
    assistant_message = {
        "id": str(uuid.uuid4()),
        "conversation_id": conversation_id,
        "role": "assistant",
        "content": ai_content,
        "citations": mock_citations,
        "created_at": datetime.utcnow().isoformat(),
    }
    messages[conversation_id].append(assistant_message)

    # Update conversation timestamp
    conversations[conversation_id]["updated_at"] = datetime.utcnow().isoformat()

    return ChatResponse(
        conversation_id=conversation_id,
        message=MessageResponse(**assistant_message),
        citations=mock_citations,
    )

# Get conversations
@app.get("/api/v1/chat/conversations", response_model=List[ConversationResponse])
async def get_conversations():
    """Get all conversations (demo mode)"""
    conv_list = list(conversations.values())
    conv_list.sort(key=lambda x: x["updated_at"], reverse=True)
    return [ConversationResponse(**conv) for conv in conv_list]

# Get single conversation with messages
@app.get("/api/v1/chat/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get a specific conversation with all messages"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conv = conversations[conversation_id]
    conv_messages = messages.get(conversation_id, [])

    return {
        **conv,
        "messages": conv_messages
    }

# Delete conversation
@app.delete("/api/v1/chat/conversations/{conversation_id}", status_code=204)
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    del conversations[conversation_id]
    if conversation_id in messages:
        del messages[conversation_id]

    return None

# Run with: uvicorn demo_server:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
