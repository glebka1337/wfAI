from app.domain.entities.user import UserProfile
from app.domain.interfaces.repositories.user import IUserProfileRepository

class UpdateUserProfileUseCase:
    def __init__(self, user_repo: IUserProfileRepository):
        self.user_repo = user_repo

    async def execute(self, profile: UserProfile) -> None:
        await self.user_repo.create_or_update(profile)
