from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.domain.entities.chat import ChatStatus

class SessionCreate(BaseModel):
    title: Optional[str] = Field(None, description="Optional initial title for the session")

class SessionUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)

class SessionSummaryResponse(BaseModel):
    uid: str
    title: str
    status: ChatStatus
    updated_at: datetime

class SessionResponse(SessionSummaryResponse):
    # Depending on requirements, full session might include messages or other heavy data
    pass

class SessionListResponse(BaseModel):
    items: List[SessionSummaryResponse]
    total: Optional[int] = None
    limit: int
    offset: int
