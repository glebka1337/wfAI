from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from app.domain.entities.base import EntityBase

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"

@dataclass(kw_only=True)
class Message(EntityBase):
    role: MessageRole
    content: str
    referenced_memory_ids: List[str] = field(default_factory=list)
    token_count: Optional[int] = None

@dataclass(kw_only=True)
class DialogSession(EntityBase):
    persona_id: str 
    title: str = "New Conversation"
    status: ChatStatus = ChatStatus.ACTIVE
    
    messages: List[Message] = field(default_factory=list)
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def add_message(self, msg: Message) -> None:
        self.messages.append(msg)
        self.updated_at = datetime.now(timezone.utc)