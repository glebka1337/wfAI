import uuid
from datetime import datetime, timezone
from typing import Annotated
from pydantic import BaseModel, Field
from beanie import Indexed

class UidMixin(BaseModel):
    uid: Annotated[str, Indexed(str, unique=True)] = Field(
        default_factory=lambda: str(uuid.uuid4())
    )

class CreatedMixin(UidMixin):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
class AuditMixin(CreatedMixin):
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))