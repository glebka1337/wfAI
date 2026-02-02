import uuid
from typing import Annotated, Optional, List
from datetime import datetime, timezone
from pydantic import Field
from beanie import Document, Indexed
from app.adapters.mongo.models.base import AuditMixin
from app.domain.entities.chat import DialogSession, Message, MessageRole, ChatStatus

# --- 1. SESSION DOC ---
class DialogSessionDoc(Document, AuditMixin):
    uid: Annotated[str, Indexed(str, unique=True)] = Field(default_factory=lambda: str(uuid.uuid4()))
    
    persona_id: Annotated[str, Indexed(str)]
    title: str
    status: str

    class Settings:
        name = "sessions"
        indexes = [
            [("persona_id", 1), ("updated_at", -1)]
        ]

    def to_entity(self) -> DialogSession:
        return DialogSession(
            uid=self.uid,
            persona_id=self.persona_id,
            title=self.title,
            status=ChatStatus(self.status),
            messages=[], 
            updated_at=self.updated_at,
            created_at=self.created_at
        )

    @classmethod
    def from_entity(cls, entity: DialogSession) -> "DialogSessionDoc":
        return cls(
            uid=entity.uid,
            persona_id=entity.persona_id,
            title=entity.title,
            status=entity.status.value,
            updated_at=entity.updated_at,
            created_at=entity.created_at
        )


class ChatMessageDoc(Document, AuditMixin):
    uid: Annotated[str, Indexed(str, unique=True)] = Field(default_factory=lambda: str(uuid.uuid4()))
    
    session_id: Annotated[str, Indexed(str)]
    
    role: str
    content: str
    
    referenced_memory_ids: List[str] = Field(default_factory=list)
    token_count: Optional[int] = None

    class Settings:
        name = "messages"
        indexes = [
            [("session_id", 1), ("created_at", 1)]
        ]

    def to_entity(self) -> Message:
        return Message(
            uid=self.uid,
            role=MessageRole(self.role),
            content=str(self.content),
            referenced_memory_ids=self.referenced_memory_ids,
            token_count=self.token_count,
            created_at=self.created_at
        )

    @classmethod
    def from_entity(cls, entity: Message, session_id: str) -> "ChatMessageDoc":
        return cls(
            uid=entity.uid,
            session_id=session_id,
            role=entity.role.value,
            content=entity.content,
            referenced_memory_ids=entity.referenced_memory_ids,
            token_count=entity.token_count,
            created_at=entity.created_at
        )