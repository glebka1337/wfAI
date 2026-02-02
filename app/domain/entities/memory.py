# app/domain/entities/memory.py
from dataclasses import dataclass, field
from typing import List, Optional
from app.domain.entities.base import EntityBase

@dataclass(kw_only=True)
class MemoryFragment(EntityBase):
    content: str
    vector_id: Optional[str] = None
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)