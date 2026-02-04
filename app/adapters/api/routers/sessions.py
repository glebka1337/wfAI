from typing import List
from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, inject

from app.adapters.api.schemas.sessions import (
    SessionListResponse, 
    SessionSummaryResponse, 
    SessionCreate, 
    SessionUpdate,
    SessionResponse
)
from app.application.usecases.session.list_sessions import ListSessionsUseCase
from app.application.usecases.session.create_session import CreateSessionUseCase
from app.application.usecases.session.delete_session import DeleteSessionUseCase
from app.application.usecases.session.update_session import UpdateSessionTitleUseCase

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.get("", response_model=SessionListResponse)
@inject
async def list_sessions(
    limit: int = 20,
    offset: int = 0,
    use_case: FromDishka[ListSessionsUseCase] = None
):
    sessions = await use_case.execute(limit, offset)
    items = [
        SessionSummaryResponse(
            uid=s.uid,
            title=s.title,
            status=s.status,
            updated_at=s.updated_at
        ) for s in sessions
    ]
    return SessionListResponse(
        items=items,
        total=len(items) + offset, # Rough estimate if total not provided by usecase
        limit=limit,
        offset=offset
    )

@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_session(
    data: SessionCreate,
    use_case: FromDishka[CreateSessionUseCase] = None
):
    uid = await use_case.execute(data.title)
    return {"uid": uid}

@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_session(
    uid: str,
    use_case: FromDishka[DeleteSessionUseCase] = None
):
    await use_case.execute(uid)

@router.patch("/{uid}")
@inject
async def update_session(
    uid: str,
    data: SessionUpdate,
    use_case: FromDishka[UpdateSessionTitleUseCase] = None
):
    await use_case.execute(uid, data.title)
    return {"status": "updated"}
