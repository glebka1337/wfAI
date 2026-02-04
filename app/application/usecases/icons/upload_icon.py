from dataclasses import dataclass
from app.domain.interfaces.repositories.icons import IWaifuIconRepository

@dataclass
class UploadIconDTO:
    filename: str
    content: bytes
    content_type: str

class UploadIconUseCase:
    def __init__(self, repository: IWaifuIconRepository):
        self.repository = repository

    async def execute(self, dto: UploadIconDTO) -> str:
        # Business Logic Validation
        ALLOWED_TYPES = ["image/png", "image/jpeg", "image/jpg"]
        if dto.content_type not in ALLOWED_TYPES:
            raise ValueError("Invalid file type. Only PNG and JPEG are allowed.")
        
        MAX_SIZE = 5 * 1024 * 1024 # 5MB
        if len(dto.content) > MAX_SIZE:
            raise ValueError("File size exceeds 5MB limit.")
            
        return await self.repository.upload_icon(dto.filename, dto.content, dto.content_type)
