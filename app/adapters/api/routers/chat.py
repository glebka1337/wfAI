from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from dishka.integrations.fastapi import FromDishka, inject

from app.adapters.api.schemas.chat import ChatStreamInput, ChatRegenerateInput, MessageResponse
from app.application.usecases.chat.process_message import ProcessMessageUseCase
from app.application.usecases.chat.regenerate import RegenerateMessageUseCase
from app.application.usecases.chat.get_history import GetChatHistoryUseCase

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/stream")
@inject
async def stream_chat(
    data: ChatStreamInput,
    use_case: FromDishka[ProcessMessageUseCase]
) -> StreamingResponse:
    return StreamingResponse(
        use_case.execute(data.message, data.session_id, data.use_search),
        media_type="text/event-stream"
    )

@router.post("/regenerate")
@inject
async def regenerate_chat(
    data: ChatRegenerateInput,
    use_case: FromDishka[RegenerateMessageUseCase]
) -> StreamingResponse:
    return StreamingResponse(
        use_case.execute(data.session_id, data.use_search),
        media_type="text/event-stream"
    )

@router.get("/{session_id}/history", response_model=List[MessageResponse])
@inject
async def get_history(
    session_id: str,
    limit: int = 20,
    older_than: Optional[datetime] = None,
    use_case: FromDishka[GetChatHistoryUseCase] = None
):
    messages = await use_case.execute(session_id, limit, older_than)
    # Mapping Domain Entities to DTOs
    return [
        MessageResponse(
            role=msg.role,
            content=msg.content,
            created_at=getattr(msg, 'created_at', None) # Depending on Message entity fields
        ) for msg in messages
    ]
