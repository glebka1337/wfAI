from app.domain.interfaces.repositories.chat import IChatRepository

class UpdateSessionTitleUseCase:
    def __init__(self, chat_repo: IChatRepository):
        self.chat_repo = chat_repo

    async def execute(self, uid: str, title: str) -> None:
        
        session = await self.chat_repo.get_session(uid)
        if session:
            session.title = title
            # DialogSession inherits from DialogSessionSummary, so this is valid.
            await self.chat_repo.update_session(session)
