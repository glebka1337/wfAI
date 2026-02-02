from typing import Annotated, List
from pydantic import Field
from beanie import Document, Indexed
from app.adapters.mongo.models.base import UidMixin
from app.domain.entities.user import UserProfile

class UserProfileDoc(Document, UidMixin):
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
            preferences=self.preferences
        )

    @classmethod
    def from_entity(cls, entity: UserProfile) -> "UserProfileDoc":
        return cls(
            uid=entity.uid,
            username=entity.username,
            bio=entity.bio,
            preferences=entity.preferences
        )