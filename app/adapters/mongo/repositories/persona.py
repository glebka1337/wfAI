from typing import List, Optional
import logging
from pymongo.errors import DuplicateKeyError # Ловим нативные ошибки БД

from app.adapters.mongo.models.persona import WaifuPersonaDoc
from app.domain.entities.persona import WaifuPersona
from app.domain.exceptions import PersonaAlreadyExists, PersoneNotFound
from app.domain.interfaces.repositories import IPersonaRepository

logger = logging.getLogger(__name__)

class MongoPersonaRepository(IPersonaRepository):
    
    async def create(self, persona: WaifuPersona) -> None:
        try:
            doc = WaifuPersonaDoc.from_entity(persona)
            await doc.insert()
        except DuplicateKeyError:
            logger.warning(f"Attempt to create duplicate persona: {persona.uid}")
            raise PersonaAlreadyExists(f"Persona {persona.uid} already exists")

    async def update(self, persona: WaifuPersona) -> None:
        doc = await WaifuPersonaDoc.find_one(WaifuPersonaDoc.uid == persona.uid)
        
        if not doc:
            logger.warning(f"Update failed: Persona {persona.uid} not found")
            raise PersoneNotFound(f"Persona {persona.uid} not found")

        doc.system_instruction = persona.system_instruction
        doc.name = persona.name
        doc.traits = persona.traits
        
        await doc.save()
    
    async def get_by_id(self, uid: str) -> Optional[WaifuPersona]:
        doc = await WaifuPersonaDoc.find_one(WaifuPersonaDoc.uid == uid)
        return doc.to_entity() if doc else None
    
    async def list_all(self, limit: int = 20, offset: int = 0) -> List[WaifuPersona]:
        docs = await WaifuPersonaDoc.find_all()\
            .skip(offset)\
            .limit(limit)\
            .to_list()
            
        return [doc.to_entity() for doc in docs]

    async def delete(self, uid: str) -> None:
        doc = await WaifuPersonaDoc.find_one(WaifuPersonaDoc.uid == uid)
        if doc:
            await doc.delete()
            logger.info(f"Persona {uid} deleted")
        else:
            logger.info(f"Delete skipped: Persona {uid} not found")