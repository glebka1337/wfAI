from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.chat import DialogSession, Message
from app.domain.entities.memory import MemoryFragment
from app.domain.entities.persona import WaifuPersona

class IPersonaRepository(ABC):
    """
    Interface for persisting Waifu personalities.
    Separates creation and updates for safety.
    """
    @abstractmethod
    async def create(self, persona: WaifuPersona) -> None:
        """
        Persist a new persona. Raises error if UID exists.
        """
        pass

    @abstractmethod
    async def update(self, persona: WaifuPersona) -> None:
        """
        Update an existing persona. Raises error if not found.
        """
        pass

    @abstractmethod
    async def get_by_id(self, uid: str) -> Optional[WaifuPersona]:
        """
        Retrieve a persona by its unique identifier.
        """
        pass

    @abstractmethod
    async def list_all(self) -> List[WaifuPersona]:
        """
        Retrieve all available personas.
        """
        pass
    
    @abstractmethod
    async def delete(self, uid: str) -> None:
        """
        Hard delete a persona configuration.
        """
        pass


class IChatRepository(ABC):
    """
    Interface for managing chat sessions and message history.
    """
    @abstractmethod
    async def create_session(self, session: DialogSession) -> None:
        """
        Initialize a new conversation thread.
        """
        pass

    @abstractmethod
    async def get_session(self, uid: str) -> Optional[DialogSession]:
        """
        Retrieve session metadata and status.
        """
        pass
    
    @abstractmethod
    async def update_session(self, session: DialogSession) -> None:
        """
        Update session details (e.g., title, status, timestamp).
        """
        pass

    @abstractmethod
    async def delete_session(self, uid: str) -> None:
        """
        Permanently remove a chat session and its messages.
        """
        pass

    @abstractmethod
    async def add_message(self, session_id: str, message: Message) -> None:
        """
        Append a message to the specific session history.
        """
        pass

    @abstractmethod
    async def get_last_messages(self, session_id: str, limit: int = 10) -> List[Message]:
        """
        Retrieve the most recent N messages for context window construction.
        """
        pass


class IMemoryRepository(ABC):
    """
    Interface for RAG (Long-Term Memory).
    Abstracts the Vector Database interactions.
    """
    @abstractmethod
    async def add_fragment(self, fragment: MemoryFragment) -> str:
        """
        Vectorize and store a memory fragment.
        Returns the internal Vector DB ID (str).
        """
        pass

    @abstractmethod
    async def search_relevant(self, query: str, limit: int = 3, threshold: float = 0.7) -> List[MemoryFragment]:
        """
        Semantic search for memory fragments.
        :param query: The user's input text to embed and search.
        :param threshold: Similarity cutoff (0.0 to 1.0).
        """
        pass
    
    @abstractmethod
    async def delete_fragment(self, vector_id: str) -> None:
        """
        Remove a specific memory fragment by its vector ID.
        """
        pass