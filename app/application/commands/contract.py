from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

ArgsSchema = TypeVar("ArgsSchema")

class ICommand(ABC, Generic[ArgsSchema]):
    """
    Interface for Slash Commands.
    
    Philosophy: "Fail Fast".
    1. Parse string into a raw dictionary (ArgsSchema).
    2. Execute logic.
    3. If data is garbage -> Raise explicit error inside execute().
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Trigger: 'remember'"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Help text: 'Usage: /remember content=... importance=...'"""
        pass

    @property
    @abstractmethod
    def args_schema(self) -> Type[ArgsSchema]:
        """TypedDict class definition."""
        pass

    @abstractmethod
    def parse_payload(self, raw_payload: str) -> ArgsSchema:
        """Splits 'key=value' string into the dict."""
        pass

    @abstractmethod
    async def execute(self, args: ArgsSchema, session_id: str) -> str:
        """
        Business logic.
        Manual validation happens here (e.g. float(args['imp'])).
        """
        pass