from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.chat import Message

class ILLMClient(ABC):
    """
    Abstraction over the LLM Provider (e.g., Ollama, vLLM).
    Strictly handles text generation.
    """
    @abstractmethod
    async def generate_response(
        self, 
        system_instruction: str, 
        history: List[Message], 
        context_fragments: List[str]
    ) -> str:
        """
        Core generation method.
        
        :param system_instruction: The raw system prompt defining the Persona.
        :param history: Recent conversation turns (Short-term memory).
        :param context_fragments: Retrieved string facts (Long-term memory).
        :return: The generated text response.
        """
        pass