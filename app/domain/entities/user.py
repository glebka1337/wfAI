# app/domain/entities/user.py
from dataclasses import dataclass, field
from typing import List
import uuid
from .base import EntityBase

@dataclass(kw_only=True)
class UserProfile:
    """
    Information about the human user.
    This data is injected into the System Prompt so the Waifu knows who she is talking to.
    """
    uid: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    bio: str = ""
    preferences: List[str] = field(default_factory=list)