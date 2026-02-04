from typing import List
from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from app.application.usecases.commands.list_commands import ListCommandsUseCase
from app.adapters.api.schemas.commands import CommandResponse

router = APIRouter(prefix="/commands", tags=["Commands"])

@router.get("", response_model=List[CommandResponse])
@inject
async def list_commands(
    use_case: FromDishka[ListCommandsUseCase]
) -> List[CommandResponse]:
    commands_dtos = await use_case.execute()
    return [
        CommandResponse(name=dto.name, description=dto.description)
        for dto in commands_dtos
    ]
