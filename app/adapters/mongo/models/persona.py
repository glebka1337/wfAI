from typing import Dict, Annotated
import uuid
from pydantic import Field
from beanie import Document, Indexed
from app.adapters.mongo.models.base import AuditMixin
from app.domain.entities.persona import WaifuPersona


class WaifuPersonaDoc(Document, AuditMixin):
    uid: Annotated[str, Indexed(str, unique=True)] = Field(
        default_factory=lambda: str(uuid.uuid4())
    )
    name: str
    system_instruction: str
    traits: Dict[str, Annotated[float, Field(ge=0.0, le=1.0)]] = Field(
        default_factory=dict
    )
    is_default: bool = False

    class Settings:
        name = "personas"

    def to_entity(self) -> WaifuPersona:
        return WaifuPersona(
            uid=self.uid,
            name=self.name,
            system_instruction=self.system_instruction,
            traits=self.traits,
            created_at=self.created_at
        )

    @classmethod
    def from_entity(cls, entity: WaifuPersona) -> "WaifuPersonaDoc":
        return cls(
            uid=entity.uid,
            name=entity.name,
            system_instruction=entity.system_instruction,
            traits=entity.traits,
            created_at=entity.created_at
        )