from app.domain.interfaces.repositories.persona import IPersonaRepository
from app.core.config import Settings

class SetPersonaIconUseCase:
    def __init__(
        self,
        persona_repo: IPersonaRepository,
        settings: Settings
    ) -> None:
        self.persona_repo = persona_repo
        self.settings = settings

    async def execute(self, icon_filename: str) -> dict:
        """Set the persona's icon URL."""
        # Get current persona
        persona = await self.persona_repo.load()
        
        # Construct the icon URL using public URL
        icon_url = f"{self.settings.S3_PUBLIC_URL}/{self.settings.S3_BUCKET_NAME}/{icon_filename}"
        
        # Update persona with new icon URL
        persona.icon_url = icon_url
        await self.persona_repo.save(persona)
        
        return {
            "uid": persona.uid,
            "name": persona.name,
            "system_instruction": persona.system_instruction,
            "traits": persona.traits,
            "icon_url": persona.icon_url
        }
