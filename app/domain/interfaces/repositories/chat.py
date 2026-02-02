from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from app.domain.entities.chat import DialogSession, DialogSessionSummary, Message

class IChatRepository(ABC):
    """
    Interface for managing chat sessions and message history.
    Strictly separates 'Summary' (Metadata) from 'DialogSession' (Aggregate with Messages).
    """

    @abstractmethod
    async def create_session(self, session: DialogSession) -> None:
        """
        Initialize a new conversation thread.
        Expects a full session object (even if messages are empty).
        """
        pass

    @abstractmethod
    async def get_session(self, uid: str) -> Optional[DialogSession]:
        """
        Retrieve a FULL session, including Initial Context (e.g. last 30 messages).
        Does NOT load full history to prevent OOM.
        """
        pass
    
    @abstractmethod
    async def get_history(
        self, 
        session_id: str, 
        limit: int = 20, 
        older_than: Optional[datetime] = None 
    ) -> List[Message]:
        pass
    
    @abstractmethod
    async def list_sessions(self, limit: int = 20, offset: int = 0) -> List[DialogSessionSummary]:
        """
        List user conversations for the sidebar/menu.
        Returns LIGHTWEIGHT summaries (no messages).
        """
        pass
    
    @abstractmethod
    async def update_session(self, session: DialogSessionSummary) -> None:
        """
        Update session metadata (title, status, persona_id).
        Accepts DialogSessionSummary (or DialogSession, since it inherits).
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
        Retrieve the most recent N messages for context window construction (LLM Context).
        """
        pass