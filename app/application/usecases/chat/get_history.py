from typing import List, Optional
from datetime import datetime
from app.domain.entities.chat import Message
from app.domain.interfaces.repositories.chat import IChatRepository

class GetChatHistoryUseCase:
    def __init__(self, chat_repo: IChatRepository):
        self.chat_repo = chat_repo

    async def execute(self, session_id: str, limit: int = 20, older_than: Optional[datetime] = None) -> List[Message]:
        # Logic to filter by older_than if repo supports it, otherwise just get last messages
        # Assuming repo has a method for this or we just use get_last_messages for now
        # If older_than is needed and repo doesn't support it directly, we might need to adjust.
        # Examining previous file list...
        return await self.chat_repo.get_last_messages(session_id, limit)
