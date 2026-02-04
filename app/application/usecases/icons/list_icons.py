from typing import List
from app.domain.interfaces.repositories.icons import IWaifuIconRepository

class ListIconsUseCase:
    def __init__(self, repository: IWaifuIconRepository):
        self.repository = repository

    async def execute(self) -> List[str]:
        return await self.repository.list_icons()
