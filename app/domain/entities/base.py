from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

@dataclass(kw_only=True)
class EntityBase:
    uid: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))