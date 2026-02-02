import uuid
from typing import Annotated, Optional, List, Union
from pydantic import Field
from beanie import Document, Indexed
from app.adapters.mongo.models.base import AuditMixin, CreatedMixin
from app.domain.entities.chat import (
    DialogSession, 
    DialogSessionSummary, 
    Message, 
    MessageRole, 
    ChatStatus
)

class DialogSessionDoc(Document, AuditMixin):
    title: str
    status: str

    class Settings:
        name = "sessions"
        indexes = [
            [("updated_at", -1)]
        ]

    def to_summary(self) -> DialogSessionSummary:
        return DialogSessionSummary(
            uid=self.uid,
            title=self.title,
            status=ChatStatus(self.status),
            updated_at=self.updated_at,
            created_at=self.created_at
        )

    def to_entity(self) -> DialogSession:
        return DialogSession(
            uid=self.uid,
            title=self.title,
            status=ChatStatus(self.status),
            messages=[], 
            updated_at=self.updated_at,
            created_at=self.created_at
        )

    @classmethod
    def from_entity(cls, entity: Union[DialogSession, DialogSessionSummary]) -> "DialogSessionDoc":
        return cls(
            uid=entity.uid,
            title=entity.title,
            status=entity.status.value,
            updated_at=entity.updated_at,
            created_at=entity.created_at
        )

class ChatMessageDoc(Document, CreatedMixin): 
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