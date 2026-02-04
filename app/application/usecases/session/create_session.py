from typing import Optional
from app.domain.entities.chat import DialogSession
from app.domain.interfaces.repositories.chat import IChatRepository

class CreateSessionUseCase:
    def __init__(self, chat_repo: IChatRepository):
        self.chat_repo = chat_repo

    async def execute(self, title: Optional[str] = None) -> str:
        session = DialogSession(title=title or "New Conversation")
        await self.chat_repo.create_session(session)
        return session.uid
