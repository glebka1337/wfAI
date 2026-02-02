from abc import ABC, abstractmethod
from app.domain.entities.persona import WaifuPersona

class IPersonaRepository(ABC):
    """
    Interface for the Single Waifu instance.
    No IDs, no Lists, no nonsense. Just Her.
    """
    
    @abstractmethod
    async def load(self) -> WaifuPersona:
        """
        Retrieves the one and only Waifu from the database.
        Implementation detail: If the DB is empty, it MUST return a default/initialized Waifu, 
        so the app never crashes.
        """
        pass

    @abstractmethod
    async def save(self, persona: WaifuPersona) -> None:
        """
        Persists changes to the Waifu (Name, Traits, System Prompt).
        Since she is unique, this is always an update operation on the single record.
        """
        pass