from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.chat import DialogSession, Message

class IChatRepository(ABC):
    """
    Interface for managing chat sessions and message history.
    """
    @abstractmethod
    async def create_session(self, session: DialogSession) -> None:
        pass

    @abstractmethod
    async def get_session(self, uid: str) -> Optional[DialogSession]:
        pass
    
    @abstractmethod
    async def list_sessions(self, limit: int = 20, offset: int = 0) -> List[DialogSession]:
        """
        List user conversations for the sidebar/menu.
        Metadata only (no messages inside).
        """
        pass
    
    @abstractmethod
    async def update_session(self, session: DialogSession) -> None:
        pass

    @abstractmethod
    async def delete_session(self, uid: str) -> None:
        pass

    @abstractmethod
    async def add_message(self, session_id: str, message: Message) -> None:
        pass

    @abstractmethod
    async def get_last_messages(self, session_id: str, limit: int = 10) -> List[Message]:
        pass