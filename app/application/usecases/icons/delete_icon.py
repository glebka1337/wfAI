from app.domain.interfaces.repositories.icons import IWaifuIconRepository

class DeleteIconUseCase:
    def __init__(self, repository: IWaifuIconRepository):
        self.repository = repository

    async def execute(self, filename: str) -> None:
        await self.repository.delete_icon(filename)
