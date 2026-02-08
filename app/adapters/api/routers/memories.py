from typing import List
from fastapi import APIRouter, Depends, Query, Path, HTTPException
from dishka.integrations.fastapi import FromDishka, inject

from app.application.usecases.memories.list_memories import ListMemoriesUseCase
from app.application.usecases.memories.delete_memory import DeleteMemoryUseCase
from app.adapters.api.schemas.memories import MemoryResponse

router = APIRouter(prefix="/memories", tags=["Memories"])

@router.get("", response_model=List[MemoryResponse])
@inject
async def list_memories(
    use_case: FromDishka[ListMemoriesUseCase],
    limit: int = Query(100, ge=1, le=1000)
) -> List[MemoryResponse]:
    fragments = await use_case.execute(limit=limit)
    return [
        MemoryResponse(
            vector_id=fragment.vector_id,
            content=fragment.content,
            importance=fragment.importance,
            created_at=fragment.created_at,
            tags=fragment.tags
        )
        for fragment in fragments
    ]

@router.delete("/{vector_id}", status_code=204)
@inject
async def delete_memory(
    vector_id: str,
    use_case: FromDishka[DeleteMemoryUseCase]
) -> None:
    await use_case.execute(vector_id)
