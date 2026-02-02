from abc import ABC, abstractmethod
from typing import List, AsyncGenerator, Dict, Any, Optional
from app.domain.entities.chat import Message

class ILLMClient(ABC):
    """
    Universal interface for interacting with a model
    """
    
    @abstractmethod
    async def stream_chat(
        self, 
        messages: List[Message], 
        system_instruction: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """
        :param messages: Session history.
        :param system_instruction: Persona prompt.
        :param model: Model name ('llama3', 'gpt-4').
        :param temperature: Creativity (0.0 - робот, 1.0 - поэт).
        :param max_tokens: Limit.
        """
        yield ""