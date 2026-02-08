"""
List memory fragments command
"""
from app.application.commands.base import BaseCommand
from app.domain.interfaces.repositories.memory import IMemoryRepository
from app.domain.entities.memory import MemoryFragment
from typing import List

class MemoryListCommand(BaseCommand):

    @property
    def name(self) -> str:
        return "memory_list"

    @property
    def description(self) -> str:
        return "Lists memory fragments"

    @property
    def args_schema(self) -> type[BaseModel]:
        return None

    def __init__(self, repository: IMemoryRepository) -> None:
        self.repository = repository
    
    async def execute(self, limit: int = 10) -> List[MemoryFragment]:
        return await self.repository.list_fragments(limit)