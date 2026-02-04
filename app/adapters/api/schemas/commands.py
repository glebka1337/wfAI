from pydantic import BaseModel

class CommandResponse(BaseModel):
    name: str
    description: str
