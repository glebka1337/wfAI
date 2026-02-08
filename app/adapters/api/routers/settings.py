from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from app.adapters.api.schemas.settings import (
    UserProfileResponse, 
    UserProfileUpdate,
    PersonaResponse, 
    PersonaUpdate
)
from app.application.usecases.settings.get_user_profile import GetUserProfileUseCase
from app.application.usecases.settings.update_user_profile import UpdateUserProfileUseCase
from app.application.usecases.settings.get_persona import GetWaifuPersonaUseCase
from app.application.usecases.settings.update_persona import UpdateWaifuPersonaUseCase
from app.application.usecases.settings.set_persona_icon import SetPersonaIconUseCase

from app.domain.entities.user import UserProfile
from app.domain.entities.persona import WaifuPersona

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/user", response_model=UserProfileResponse)
@inject
async def get_user_profile(
    use_case: FromDishka[GetUserProfileUseCase] = None
):
    profile = await use_case.execute()
    # Handle possible None if logic allows, though Repo says "get_default" usually.
    # Assuming profile is not None for simplicity or we handle default in UseCase/Repo.
    # But repository interface returns Optional. 
    # UseCase implementation returned exactly what Repo returned.
    # We should handle it here to ensure response model match.
    if not profile:
        # Should not happen in single-user app if we bootstrap correctly, 
        # but let's provide default
        return UserProfileResponse(uid="", username="User", bio="", preferences=[])
        
    return UserProfileResponse(
        uid=profile.uid,
        username=profile.username,
        bio=profile.bio,
        preferences=profile.preferences
    )

@router.patch("/user")
@inject
async def update_user_profile(
    data: UserProfileUpdate,
    use_case: FromDishka[UpdateUserProfileUseCase] = None,
    get_use_case: FromDishka[GetUserProfileUseCase] = None
):
    # Fetch existing to update partial
    current = await get_use_case.execute() or UserProfile(username="User")
    
    # Apply updates
    if data.username is not None:
        current.username = data.username
    if data.bio is not None:
        current.bio = data.bio
    if data.preferences is not None:
        current.preferences = data.preferences
        
    await use_case.execute(current)
    return {"status": "updated"}

@router.get("/waifu", response_model=PersonaResponse)
@inject
async def get_waifu_persona(
    use_case: FromDishka[GetWaifuPersonaUseCase] = None
):
    persona = await use_case.execute()
    return PersonaResponse(
        uid=persona.uid,
        name=persona.name,
        system_instruction=persona.system_instruction,
        traits=persona.traits,
        icon_url=persona.icon_url,
        language=persona.language
    )

@router.patch("/waifu")
@inject
async def update_waifu_persona(
    data: PersonaUpdate,
    use_case: FromDishka[UpdateWaifuPersonaUseCase] = None,
    get_use_case: FromDishka[GetWaifuPersonaUseCase] = None
):
    current = await get_use_case.execute()
    
    if data.name is not None:
        current.name = data.name
    if data.system_instruction is not None:
        current.system_instruction = data.system_instruction
    if data.traits is not None:
        current.traits = data.traits
        
    await use_case.execute(current)
    return {"status": "updated"}

@router.patch("/waifu/icon", response_model=PersonaResponse)
@inject
async def set_waifu_icon(
    icon_filename: str,
    use_case: FromDishka[SetPersonaIconUseCase] = None
):
    """Set the persona's icon by filename."""
    result = await use_case.execute(icon_filename)
    return PersonaResponse(**result)
