from dataclasses import dataclass, field
from typing import Dict
from app.domain.entities.base import EntityBase

@dataclass(kw_only=True)
class WaifuPersona(EntityBase):
    name: str
    system_instruction: str
    traits: Dict[str, float] = field(default_factory=dict)