from typing import Type
from pydantic import BaseModel, Field

from app.application.commands.base import BaseCommand
from app.domain.interfaces.repositories.memory import IMemoryRepository
from app.domain.entities.memory import MemoryFragment

class RememberArgs(BaseModel):
    content: str = Field(..., description="The information to save.")
    importance: float = Field(0.5, ge=0.0, le=1.0, description="Importance weight (0.0 to 1.0).")

class RememberCommand(BaseCommand[RememberArgs]):
    
    @property
    def name(self) -> str:
        return "remember"

    @property
    def description(self) -> str:
        return (
            "Remembers certain facts.\n"
            "Params:\n"
            "content - what to remember\n"
            "importance - scale from 0 to 1"
        )
    
    @property
    def args_schema(self) -> type[RememberArgs]:
        return RememberArgs

    def __init__(self, memory_repo: IMemoryRepository):
        self.memory_repo = memory_repo

    async def execute(self, args: RememberArgs, session_id: str) -> str:
        fragment = MemoryFragment(
            content=args.content,
            importance=args.importance,
            tags=["user_command"]
        )
        
        await self.memory_repo.add_fragment(fragment)
        return f"Saved: '{args.content}' (Imp: {args.importance})"