from typing import List
from app.domain.entities.memory import MemoryFragment
from app.domain.interfaces.repositories.memory import IMemoryRepository

class ListMemoriesUseCase:
    def __init__(self, repository: IMemoryRepository):
        self.repository = repository

    async def execute(self, limit: int = 100) -> List[MemoryFragment]:
        return await self.repository.list_fragments(limit=limit)
