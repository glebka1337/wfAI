import logging
from typing import Optional
from app.adapters.mongo.models.user import UserProfileDoc
from app.domain.entities.user import UserProfile
from app.domain.interfaces.repositories.user import IUserProfileRepository

logger = logging.getLogger(__name__)

class MongoUserProfileRepository(IUserProfileRepository):
    """
    Implementation of User Profile Persistence.
    """

    async def create_or_update(self, profile: UserProfile) -> None:
        # Try to find by UID
        doc = await UserProfileDoc.find_one(UserProfileDoc.uid == profile.uid)
        
        if doc:
            # Update
            doc.username = profile.username
            doc.bio = profile.bio
            doc.preferences = profile.preferences
            await doc.save()
            logger.info(f"User profile '{profile.username}' updated.")
        else:
            # Create
            new_doc = UserProfileDoc.from_entity(profile)
            await new_doc.insert()
            logger.info(f"User profile '{profile.username}' created.")

    async def get_default(self) -> Optional[UserProfile]:
        """
        Fetch the first available user profile.
        """
        doc = await UserProfileDoc.find_all().first_or_none()
        return doc.to_entity() if doc else None