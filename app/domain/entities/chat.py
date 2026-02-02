# app/domain/entities/chat.py
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from .base import EntityBase

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
class DialogSessionSummary(EntityBase):
    """
    Lightweight entity for lists/sidebars.
    Contains NO messages, preventing 'Phantom Message' bugs.
    """
    persona_id: str 
    title: str = "New Conversation"
    status: ChatStatus = ChatStatus.ACTIVE
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass(kw_only=True)
class DialogSession(DialogSessionSummary):
    """
    Full entity for active chat interaction.
    Guaranteed to have a list of messages (even if empty, it's a valid list).
    """
    messages: List[Message] = field(default_factory=list)

    def add_message(self, msg: Message) -> None:
        self.messages.append(msg)
        self.updated_at = datetime.now(timezone.utc)