from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar

ArgsSchema = TypeVar("ArgsSchema") # in future it can be Pydantic / dict / dataclass

class BaseTool(ABC, Generic[ArgsSchema]):
    """
    Pure, Library-Agnostic Interface for AI Tools.
    
    Uses Python Generics to define the input contract.
    The responsibility of converting 'T' to JSON Schema lies with the Adapter,
    not the Domain Entity.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique identifier (e.g., 'calculate_sum').
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Intent description for the LLM.
        """
        pass

    @property
    @abstractmethod
    def args_schema(self) -> Type[ArgsSchema]:
        """
        Returns the Class definition of the arguments.
        
        Examples:
        - return MyPydanticModel
        - return MyDataclass
        """
        pass

    @abstractmethod
    async def execute(self, args: ArgsSchema) -> Any:
        """
        Execute the tool logic.
        :param args: An instance of T (already validated and parsed by the Adapter).
        """
        pass