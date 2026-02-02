from typing import Annotated, List
import uuid
from pydantic import Field
from beanie import Document, Indexed
from app.adapters.mongo.models.base import AuditMixin
from app.domain.entities.user import UserProfile

class UserProfileDoc(Document, AuditMixin):
    uid: Annotated[str, Indexed(str, unique=True)] = Field(
        default_factory=lambda: str(uuid.uuid4())
    )

    username: Annotated[str, Indexed(str, unique=True)] 
    bio: str = ""
    preferences: List[str] = Field(default_factory=list)

    class Settings:
        name = "users"
        
    def to_entity(self) -> UserProfile:
        return UserProfile(
            uid=self.uid,
            username=self.username,
            bio=self.bio,
            preferences=self.preferences,
            created_at=self.created_at
        )

    @classmethod
    def from_entity(cls, entity: UserProfile) -> "UserProfileDoc":
        return cls(
            uid=entity.uid,
            username=entity.username,
            bio=entity.bio,
            preferences=entity.preferences,
            created_at=entity.created_at
        )