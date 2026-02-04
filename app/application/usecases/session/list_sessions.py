from typing import List
from app.domain.entities.chat import DialogSessionSummary
from app.domain.interfaces.repositories.chat import IChatRepository

class ListSessionsUseCase:
    def __init__(self, chat_repo: IChatRepository):
        self.chat_repo = chat_repo

    async def execute(self, limit: int = 20, offset: int = 0) -> List[DialogSessionSummary]:
        return await self.chat_repo.list_sessions(limit, offset)
