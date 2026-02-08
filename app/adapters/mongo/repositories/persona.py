import logging
from typing import Optional
from app.adapters.mongo.models.persona import WaifuPersonaDoc
from app.domain.entities.persona import WaifuPersona
from app.domain.interfaces.repositories.persona import IPersonaRepository

logger = logging.getLogger(__name__)

class MongoPersonaRepository(IPersonaRepository):
    """
    Implementation of Single Waifu Persistence using MongoDB.
    Acts as a Singleton store.
    """
    
    async def load(self) -> WaifuPersona:
        """
        Retrieves the Waifu. If none exists, creates a default one.
        """
        # Try to find any persona (since we only have one)
        doc = await WaifuPersonaDoc.find_all().first_or_none()
        
        if doc:
            return doc.to_entity()
        
        # Fallback: Initialize default Waifu if DB is empty
        logger.info("No Waifu found in DB. Initializing default persona.")
        default_persona = WaifuPersona(
            name="Rebecca",
            system_instruction="You are Rebecca, a sharp-tongued but caring assistant.",
            traits={"sharpness": 0.8, "intellect": 0.9}
        )
        # Persist it immediately so next time we find it
        new_doc = WaifuPersonaDoc.from_entity(default_persona)
        await new_doc.insert()
        
        return default_persona

    async def save(self, persona: WaifuPersona) -> None:
        """
        Persists changes. Uses UPSERT logic based on UID.
        """
        doc = await WaifuPersonaDoc.find_one(WaifuPersonaDoc.uid == persona.uid)
        
        if doc:
            # Update existing
            doc.name = persona.name
            doc.system_instruction = persona.system_instruction
            doc.traits = persona.traits
            doc.icon_url = persona.icon_url
            doc.language = persona.language
            await doc.save()
            logger.info(f"Waifu '{persona.name}' updated.")
        else:
            # Create new (rare case if load() wasn't called first)
            new_doc = WaifuPersonaDoc.from_entity(persona)
            await new_doc.insert()
            logger.info(f"Waifu '{persona.name}' saved as new record.")