from abc import ABC, abstractmethod
from typing import AsyncGenerator

class IChatService(ABC):
    """
    Business Logic Interface.
    """
    
    @abstractmethod
    async def create_chat(self, user_id: str = "default") -> str:
        """Creates a new session and returns its UID."""
        pass

    @abstractmethod
    async def send_message(
        self, 
        user_id: str,
        session_id: str, 
        user_text: str
    ) -> AsyncGenerator[str, None]:
        """
        Main flow: User -> RAG -> Context -> LLM -> Stream.
        """
        pass
    
    @abstractmethod
    async def save_memory(self, content: str) -> None:
        """User manually saves something important."""
        pass