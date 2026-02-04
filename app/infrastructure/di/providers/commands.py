from typing import Iterable, List
from dishka import Provider, Scope, provide

from app.application.commands.contract import ICommand
from app.application.commands.registry import CommandRegistry

# Command Implementations
from app.application.commands.implementations.remember import RememberCommand
from app.domain.interfaces.repositories.memory import IMemoryRepository

class CommandsProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_remember_command(self, memory_repo: IMemoryRepository) -> RememberCommand:
        return RememberCommand(memory_repo)

    @provide
    def provide_command_registry(self, cmd: RememberCommand) -> CommandRegistry:
        # If we have multiple commands, we'd request them all here
        # Dishka doesn't support list collection automatically unless configured, 
        # so we explicitly list them or use a multi-provider pattern if needed.
        # For now, explicit is fine.
        return CommandRegistry(commands=[cmd])
