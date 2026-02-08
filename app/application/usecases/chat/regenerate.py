from typing import AsyncGenerator
from app.domain.entities.chat import MessageRole
from app.domain.interfaces.repositories.chat import IChatRepository
from app.application.usecases.chat.process_message import ProcessMessageUseCase

class RegenerateMessageUseCase:
    """
    Orchestrates the regeneration of the last AI response.
    1. Removes the last AI message.
    2. Retrieves the previous User message.
    3. Re-runs ProcessMessageUseCase logic (without saving the user message again).
    """
    
    def __init__(
        self,
        chat_repo: IChatRepository,
        process_message_use_case: ProcessMessageUseCase
    ):
        self.chat_repo = chat_repo
        self.process_message_uc = process_message_use_case
        
    async def execute(self, session_id: str, use_search: bool = False) -> AsyncGenerator[str, None]:
        # 1. Get last message to see if we can regenerate
        last_msgs = await self.chat_repo.get_last_messages(session_id, limit=1)
        
        if not last_msgs:
            yield "Wait... I don't remember anything to regenerate."
            return

        last_msg = last_msgs[-1]
        
        # 2. Logic:
        # If last is AI => Delete AI msg -> Get User Msg -> Run Process(save=False)
        # If last is User => Run Process(save=False) (User clicked regenerate on their own pending msg? or failed previous attempt?)
        # Let's support "Delete AI" scenario primarily.
        
        user_prompt = ""
        
        if last_msg.role == MessageRole.ASSISTANT:
            # Delete it
            await self.chat_repo.delete_last_message(session_id)
            # Fetch previous user message
            last_msgs = await self.chat_repo.get_last_messages(session_id, limit=1)
            if not last_msgs or last_msgs[-1].role != MessageRole.USER:
                yield "I can't find your original message to retry."
                return
            user_prompt = last_msgs[-1].content
            
        elif last_msg.role == MessageRole.USER:
            # Just re-run for this user message
            # But we don't delete it.
            user_prompt = last_msg.content
        else:
             # System message?
             yield "I can't regenerate system messages."
             return

        # 3. Call ProcessMessage logic
        # We set save_user_input=False because the user message is already in DB.
        async for chunk in self.process_message_uc.execute(
            message_text=user_prompt, 
            session_id=session_id, 
            use_search=use_search, 
            save_user_input=False
        ):
            yield chunk
