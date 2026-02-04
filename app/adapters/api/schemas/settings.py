from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    preferences: Optional[List[str]] = None

class UserProfileResponse(BaseModel):
    uid: str
    username: str
    bio: str
    preferences: List[str]

class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    system_instruction: Optional[str] = None
    traits: Optional[Dict[str, float]] = None

class PersonaResponse(BaseModel):
    uid: str
    name: str
    system_instruction: str
    traits: Dict[str, float]
    icon_url: Optional[str] = None
