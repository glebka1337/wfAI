from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import UserProfile

class IUserProfileRepository(ABC):
    """
    Interface for User Profile management.
    In 'Single User Mode', we often just need 'get_default'.
    """
    @abstractmethod
    async def create_or_update(self, profile: UserProfile) -> None:
        """
        Since we have one user, this is an upsert operation.
        """
        pass

    @abstractmethod
    async def get_default(self) -> Optional[UserProfile]:
        """
        Get the main (and likely only) user profile.
        """
        pass