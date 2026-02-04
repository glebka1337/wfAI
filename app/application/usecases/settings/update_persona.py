from app.domain.entities.persona import WaifuPersona
from app.domain.interfaces.repositories.persona import IPersonaRepository

class UpdateWaifuPersonaUseCase:
    def __init__(self, persona_repo: IPersonaRepository):
        self.persona_repo = persona_repo

    async def execute(self, persona: WaifuPersona) -> None:
        await self.persona_repo.save(persona)
