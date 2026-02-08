from abc import ABC, abstractmethod

class ISearchTool(ABC):
    @abstractmethod
    async def search(self, query: str) -> str:
        """
        Perform a search and return a formatted string summary of results.
        """
        pass
