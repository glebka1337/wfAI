from typing import Optional
from app.domain.entities.user import UserProfile
from app.domain.interfaces.repositories.user import IUserProfileRepository

class GetUserProfileUseCase:
    def __init__(self, user_repo: IUserProfileRepository):
        self.user_repo = user_repo

    async def execute(self) -> Optional[UserProfile]:
        return await self.user_repo.get_profile()
