from abc import ABC, abstractmethod
from typing import List

class IWaifuIconRepository(ABC):
    @abstractmethod
    async def upload_icon(self, filename: str, content: bytes, content_type: str) -> str:
        """
        Uploads an icon and returns the public URL.
        """
        pass

    @abstractmethod
    async def list_icons(self) -> List[str]:
        """
        Returns a list of public URLs for all uploaded icons.
        """
        pass

    @abstractmethod
    async def delete_icon(self, filename: str) -> None:
        """
        Deletes an icon by filename.
        """
        pass
