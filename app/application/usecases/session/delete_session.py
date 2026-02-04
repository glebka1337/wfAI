from app.domain.interfaces.repositories.chat import IChatRepository

class DeleteSessionUseCase:
    def __init__(self, chat_repo: IChatRepository):
        self.chat_repo = chat_repo

    async def execute(self, uid: str) -> None:
        await self.chat_repo.delete_session(uid)
