import logging
from app.domain.entities.user import UserProfile
from app.domain.interfaces.repositories.user import IUserProfileRepository
from app.domain.interfaces.repositories.persona import IPersonaRepository

logger = logging.getLogger(__name__)

class AppBootstrapper:
    def __init__(
        self,
        user_repo: IUserProfileRepository,
        persona_repo: IPersonaRepository
    ):
        self.user_repo = user_repo
        self.persona_repo = persona_repo

    async def run(self):
        """
        Ensures that necessary default data exists in the database.
        """
        logger.info("Running App Bootstrapper...")
        
        # 1. Ensure User Profile exists
        existing_user = await self.user_repo.get_profile()
        if not existing_user:
            logger.info("No user profile found. Creating default user.")
            default_user = UserProfile(
                username="User",
                bio="I am a curious human.",
                preferences=["friendly", "concise"]
            )
            await self.user_repo.create_or_update(default_user)
        else:
            logger.info(f"User profile found: {existing_user.username}")

        # 2. Ensure Waifu Persona exists (Repo implementation handles default creation on load)
        # Calling load() triggers the auto-creation logic in MongoPersonaRepository if missing.
        persona = await self.persona_repo.load()
        logger.info(f"Waifu Persona ready: {persona.name}")
        
        logger.info("App Bootstrapper finished.")
