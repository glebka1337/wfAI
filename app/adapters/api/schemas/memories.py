from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class MemoryResponse(BaseModel):
    vector_id: Optional[str]
    content: str
    importance: float
    created_at: datetime
    tags: List[str] = []
