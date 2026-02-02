from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.persona import WaifuPersona

class IPersonaRepository(ABC):
    """
    Interface for persisting Waifu personalities.
    """
    @abstractmethod
    async def create(self, persona: WaifuPersona) -> None:
        pass

    @abstractmethod
    async def update(self, persona: WaifuPersona) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, uid: str) -> Optional[WaifuPersona]:
        pass

    @abstractmethod
    async def list_all(self, limit: int = 20, offset: int = 0) -> List[WaifuPersona]:
        """
        Retrieve available personas with pagination.
        :param limit: Max items to fetch (default 20).
        :param offset: Number of items to skip.
        """
        pass
    
    @abstractmethod
    async def delete(self, uid: str) -> None:
        pass