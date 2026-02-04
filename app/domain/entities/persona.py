# app/domain/entities/persona.py
from dataclasses import dataclass, field
from typing import Dict, Optional
import uuid
from app.domain.entities.base import EntityBase

@dataclass(kw_only=True)
class WaifuPersona:
    uid: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    system_instruction: str
    traits: Dict[str, float] = field(default_factory=dict)
    icon_url: Optional[str] = None