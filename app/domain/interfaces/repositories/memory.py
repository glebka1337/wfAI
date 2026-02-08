from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.memory import MemoryFragment

class IMemoryRepository(ABC):
    """
    Interface for RAG (Long-Term Memory).
    """
    @abstractmethod
    async def add_fragment(self, fragment: MemoryFragment) -> str:
        pass

    @abstractmethod
    async def search_relevant(self, query: str, limit: int = 3, threshold: float = 0.7) -> List[MemoryFragment]:
        pass
    
    @abstractmethod
    async def delete_fragment(self, vector_id: str) -> None:
        pass

    @abstractmethod
    async def list_fragments(self, limit: int = 10) -> List[MemoryFragment]:
        """
        Returns a list of memory fragments with limit specified.
        """
        pass