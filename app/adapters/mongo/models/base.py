import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class CreatedMixin(BaseModel):
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
class AuditMixin(CreatedMixin):
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))