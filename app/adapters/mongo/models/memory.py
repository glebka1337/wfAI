from typing import List, Optional, Annotated
from beanie import Document, Indexed
from app.domain.entities.memory import MemoryFragment
from .base import CreatedMixin

class MemoryFragmentDoc(Document, CreatedMixin):
    content: str
    vector_id: Optional[Annotated[str, Indexed(str)]] = None
    importance: float = 0.5
    tags: List[str] = []

    class Settings:
        name = "memories"

    def to_entity(self) -> MemoryFragment:
        return MemoryFragment(
            uid=self.uid,
            content=self.content,
            vector_id=self.vector_id,
            importance=self.importance,
            tags=self.tags,
            created_at=self.created_at
        )

    @classmethod
    def from_entity(cls, entity: MemoryFragment) -> "MemoryFragmentDoc":
        return cls(
            uid=entity.uid,
            content=entity.content,
            vector_id=entity.vector_id,
            importance=entity.importance,
            tags=entity.tags,
            created_at=entity.created_at
        )