from app.domain.interfaces.repositories.memory import IMemoryRepository

class DeleteMemoryUseCase:
    def __init__(self, repository: IMemoryRepository):
        self.repository = repository

    async def execute(self, vector_id: str) -> None:
        await self.repository.delete_fragment(vector_id)
