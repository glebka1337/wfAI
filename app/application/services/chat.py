import logging
from typing import AsyncGenerator, List
from app.core.config import settings
from app.domain.entities.chat import Message, MessageRole, DialogSession
from app.domain.interfaces.services.chat import IChatService
from app.domain.interfaces.repositories.chat import IChatRepository
from app.domain.interfaces.repositories.persona import IPersonaRepository
from app.domain.interfaces.repositories.user import IUserProfileRepository
from app.domain.interfaces.llm import ILLMClient

logger = logging.getLogger(__name__)

class ChatService(IChatService):
    def __init__(
        self, 
        chat_repo: IChatRepository, 
        persona_repo: IPersonaRepository,
        user_repo: IUserProfileRepository,
        llm_client: ILLMClient,
    ):
        self.chat_repo = chat_repo
        self.persona_repo = persona_repo
        self.user_repo = user_repo
        self.llm_client = llm_client

    def _build_system_prompt(self, persona_prompt: str, user_bio: str, user_name: str) -> str:
        return (
            f"{persona_prompt}\n\n"
            f"=== USER CONTEXT ===\n"
            f"User Name: {user_name}\n"
            f"User Info: {user_bio}\n"
            f"Instructions: Use User Info to personalize your answers. Remember that you are talking to {user_name}."
        )

    def _prune_context(
        self, 
        history: List[Message], 
        system_instruction: str, 
        new_user_msg: Message
    ) -> List[Message]:
        
        current_char_count = len(system_instruction) + len(new_user_msg.content)
        allowed_history = []
        
        for msg in reversed(history):
            msg_len = len(msg.content)
            if current_char_count + msg_len < settings.CONTEXT_CHAR_LIMIT:
                allowed_history.insert(0, msg)
                current_char_count += msg_len
            else:
                break
        return allowed_history

    async def create_chat(self, user_id: str = "default") -> str:
        # В режиме Моногамии user_id не так важен, но для совместимости оставим
        session = DialogSession(
            user_id=user_id,
            title="New Conversation"
        )
        await self.chat_repo.create_session(session)
        return session.uid

    async def send_message(
        self, 
        user_id: str,
        session_id: str, 
        user_text: str
    ) -> AsyncGenerator[str, None]:
        
        # 1. Load Session
        session = await self.chat_repo.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        # 2. Load Single Waifu (No ID needed)
        persona = await self.persona_repo.load()
        
        # 3. Load Single User (No ID needed, just default)
        user_profile = await self.user_repo.get_profile()
        
        # Fallback values if user profile is empty
        u_name = user_profile.username if user_profile else "User"
        u_bio = user_profile.bio if user_profile else ""
        
        # 4. Construct System Prompt
        full_system_instruction = self._build_system_prompt(
            persona.system_instruction, u_bio, u_name
        )

        # 5. Prepare Message
        user_msg = Message(role=MessageRole.USER, content=user_text)
        
        # 6. Context & Pruning
        raw_history = await self.chat_repo.get_last_messages(session_id, limit=settings.INITIAL_HISTORY_DEPTH)
        final_context = self._prune_context(raw_history, full_system_instruction, user_msg)
        final_context.append(user_msg)

        # 7. Save User Message
        await self.chat_repo.add_message(session_id, user_msg)
        
        # 8. Stream LLM
        full_response = ""
        try:
            stream = self.llm_client.stream_chat(
                messages=final_context,
                system_instruction=full_system_instruction,
                model=settings.DEFAULT_MODEL,
                temperature=settings.LLM_TEMPERATURE
            )
            
            async for chunk in stream:
                full_response += chunk
                yield chunk
                
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            yield f"[Error: {e}]"

        # 9. Save Assistant Response
        if full_response:
            asst_msg = Message(role=MessageRole.ASSISTANT, content=full_response)
            await self.chat_repo.add_message(session_id, asst_msg)