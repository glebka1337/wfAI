from app.domain.entities.persona import WaifuPersona
from app.domain.interfaces.repositories.persona import IPersonaRepository

class GetWaifuPersonaUseCase:
    def __init__(self, persona_repo: IPersonaRepository):
        self.persona_repo = persona_repo

    async def execute(self) -> WaifuPersona:
        return await self.persona_repo.load()
