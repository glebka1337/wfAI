from dataclasses import dataclass
from typing import List
from app.application.commands.registry import CommandRegistry

@dataclass
class CommandDTO:
    name: str
    description: str

class ListCommandsUseCase:
    def __init__(self, registry: CommandRegistry) -> None:
        self.registry = registry

    async def execute(self) -> List[CommandDTO]:
        commands = self.registry.get_commands()
        return [
            CommandDTO(name=cmd.name, description=cmd.description)
            for cmd in commands
        ]
