from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from dishka.integrations.fastapi import FromDishka, inject

from app.application.usecases.icons.upload_icon import UploadIconUseCase, UploadIconDTO
from app.application.usecases.icons.list_icons import ListIconsUseCase
from app.application.usecases.icons.delete_icon import DeleteIconUseCase

router = APIRouter(prefix="/icons", tags=["Waifu Icons"])

@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def upload_icon(
    file: UploadFile = File(...),
    use_case: FromDishka[UploadIconUseCase] = None
):
    try:
        content = await file.read()
        dto = UploadIconDTO(
            filename=file.filename,
            content=content,
            content_type=file.content_type
        )
        url = await use_case.execute(dto)
        return {"url": url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[str])
@inject
async def list_icons(
    use_case: FromDishka[ListIconsUseCase] = None
):
    return await use_case.execute()

@router.delete("/{filename}")
@inject
async def delete_icon(
    filename: str,
    use_case: FromDishka[DeleteIconUseCase] = None
):
    await use_case.execute(filename)
    return {"status": "deleted"}
