from dataclasses import dataclass, field
from typing import List, Optional
from .base import EntityBase

@dataclass(kw_only=True)
class UserProfile(EntityBase):
    """
    Information about the human user.
    This data is injected into the System Prompt so the Waifu knows who she is talking to.
    """
    username: str
    bio: str = ""
    preferences: List[str] = field(default_factory=list)