from typing import Dict, Annotated
from pydantic import Field
from beanie import Document
from app.adapters.mongo.models.base import UidMixin
from app.domain.entities.persona import WaifuPersona

class WaifuPersonaDoc(Document, UidMixin):
    name: str
    system_instruction: str
    traits: Dict[str, Annotated[float, Field(ge=0.0, le=1.0)]] = Field(
        default_factory=dict
    )
    is_default: bool = False
    icon_url: str | None = None
    language: str = "English"

    class Settings:
        name = "personas"

    def to_entity(self) -> WaifuPersona:
        return WaifuPersona(
            uid=self.uid,
            name=self.name,
            system_instruction=self.system_instruction,
            traits=self.traits,
            icon_url=self.icon_url,
            language=self.language
        )

    @classmethod
    def from_entity(cls, entity: WaifuPersona) -> "WaifuPersonaDoc":
        return cls(
            uid=entity.uid,
            name=entity.name,
            system_instruction=entity.system_instruction,
            traits=entity.traits,
            icon_url=entity.icon_url,
            language=entity.language
        )