import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class AuditMixin(BaseModel):
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))