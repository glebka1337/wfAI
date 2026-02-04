from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.domain.entities.chat import MessageRole

class ChatStreamInput(BaseModel):
    message: str = Field(..., min_length=1, description="User message content")
    session_id: str = Field(..., description="ID of the chat session")

class MessageResponse(BaseModel):
    role: MessageRole
    content: str
    created_at: Optional[datetime] = None
