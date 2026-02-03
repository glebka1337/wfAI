from abc import ABC, abstractmethod

class IEmbedder(ABC):
    @abstractmethod
    async def get_vector(self, text: str) -> list[float]:
        pass