import logging
from typing import AsyncGenerator
from datetime import datetime

from app.domain.entities.chat import Message, MessageRole
from app.domain.entities.user import UserProfile
from app.domain.entities.persona import WaifuPersona

from app.domain.interfaces.llm import ILLMClient
from app.domain.interfaces.repositories.memory import IMemoryRepository
from app.domain.interfaces.repositories.chat import IChatRepository
from app.domain.interfaces.repositories.user import IUserProfileRepository
from app.domain.interfaces.repositories.persona import IPersonaRepository
from app.domain.interfaces.tools.search import ISearchTool

from app.application.commands.registry import CommandRegistry
from app.core.config import settings

logger = logging.getLogger(__name__)

class ProcessMessageUseCase:
    
    def __init__(
        self,
        registry: CommandRegistry,
        memory_repo: IMemoryRepository,
        history_repo: IChatRepository,
        user_repo: IUserProfileRepository,
        persona_repo: IPersonaRepository,
        llm_client: ILLMClient,
        search_tool: ISearchTool = None # Optional for now to avoid breaking tests/DI immediately
    ):
        self.registry = registry
        self.memory_repo = memory_repo
        self.history_repo = history_repo
        self.user_repo = user_repo
        self.persona_repo = persona_repo
        self.llm_client = llm_client
        self.search_tool = search_tool

    async def execute(
        self, 
        message_text: str, 
        session_id: str,
        use_search: bool = False,
        save_user_input: bool = True
    ) -> AsyncGenerator[str, None]:
        
        cmd_res = await self.registry.process_input(message_text, session_id)
        if cmd_res:
            yield cmd_res
            return

        if save_user_input:
            await self._save_user_message(session_id, message_text)

        import asyncio
        
        user_task = self.user_repo.get_profile()
        persona_task = self.persona_repo.load()
        memory_task = self.memory_repo.search_relevant(message_text, limit=3)
        history_task = self.history_repo.get_last_messages(session_id, limit=10)
        
        user_profile, waifu_persona, relevant_memories, chat_history = await asyncio.gather(
            user_task, 
            persona_task, 
            memory_task, 
            history_task
        )
        
        user_profile = user_profile or self._default_user()

        system_prompt = await self._build_prompt(
            user=user_profile,
            waifu=waifu_persona,
            memories=relevant_memories
        )

        if not chat_history:
            chat_history = [Message(role=MessageRole.USER, content=message_text)]

        # --- MANUAL SEARCH LOGIC ---
        if use_search and self.search_tool:
            # 1. Inform user we are searching
            yield "\n*(Searching the web...)*\n\n"
            
            # 2. Generate optimized query
            # We use a simple non-streaming call to LLM to get the query
            search_prompt = (
                f"Act as a Search Engine Query Optimizer.\n"
                f"User's raw message: '{message_text}'.\n"
                f"Chat Context: {chat_history[-2].content if len(chat_history) > 1 else 'None'}.\n"
                f"User Preferences: {', '.join(user_profile.preferences) if user_profile.preferences else 'None'}.\n\n"
                f"Task: Transform the raw message into a concise, keyword-focused web search query.\n"
                f"Rules:\n"
                f"1. Remove conversational filler ('I wonder', 'maybe', 'hello').\n"
                f"2. Focus on the core intent.\n"
                f"3. Use the SAME language as the user's message.\n"
                f"4. If the request is vague, use User Preferences to make it specific (e.g. 'popular music' -> 'popular phonk music' if user likes phonk).\n"
                f"Output: ONLY the final query string."
            )
            # Temporary messages for query generation
            query_msgs = [Message(role=MessageRole.USER, content=search_prompt)]
            
            # We need a non-streaming method on llm_client or just consume the stream
            search_query = ""
            async for chunk in self.llm_client.stream_chat(messages=query_msgs, system_instruction="You are a helpful query generator.", model=settings.DEFAULT_MODEL):
                search_query += chunk
            
            search_query = search_query.strip().strip('"').strip("'")
            yield f"*(Query: {search_query})*\n\n"

            # 3. Execute Search
            search_results = await self.search_tool.search(search_query)

            # 4. Inject results as System Message
            results_msg = Message(
                role=MessageRole.SYSTEM, 
                content=f"WEB SEARCH RESULTS for '{search_query}':\n{search_results}\n\n"
                        f"INSTRUCTION: Use the above results to answer the user's last message."
            )
            chat_history.append(results_msg)

        # --- FINAL RESPONSE GENERATION ---
        full_response = ""
        async for chunk in self.llm_client.stream_chat(
            messages=chat_history,
            system_instruction=system_prompt,
            model=settings.DEFAULT_MODEL
        ):
            full_response += chunk
            yield chunk

        if full_response:
            await self._save_ai_message(session_id, full_response)

    async def _build_prompt(
        self, 
        user: UserProfile, 
        waifu: WaifuPersona, 
        memories: list
    ) -> str:
        
        rag_content = "\n".join([f"- {m.content}" for m in memories]) if memories else "No relevant memories."
        traits_list = [f"{k}: {v:.2f}" for k, v in waifu.traits.items()]
        traits_str = ", ".join(traits_list)
        current_dt = datetime.now().strftime('%Y-%m-%d %H:%M (%A)')
        
        lang = waifu.language if waifu.language else 'English'

        return (
            f"Roleplay Instructions:\n"
            f"You are {waifu.name}. {waifu.system_instruction}\n"
            f"Your personality traits (scale 0.0-1.0): {traits_str}.\n"
            f"Note: 0.0 means the trait is absent, 1.0 means it is extremely dominant.\n"
            f"IMPORTANT: Always respond in {lang}.\n\n"
            f"IMPORTANT: Always respond in {lang}.\n\n"
            f"User Profile:\n"
            f"Name: {user.username}\n"
            f"Bio: {user.bio}\n"
            f"Preferences: {', '.join(user.preferences)}\n\n"
            f"Context / Memories:\n{rag_content}\n\n"
            f"Current Date/Time: {current_dt}\n"
            f"Reply to the user naturally based on the history."
        )

    async def _save_user_message(self, session_id: str, text: str):
        msg = Message(role=MessageRole.USER, content=text, created_at=datetime.utcnow())
        await self.history_repo.add_message(session_id, msg)

    async def _save_ai_message(self, session_id: str, text: str):
        msg = Message(role=MessageRole.ASSISTANT, content=text, created_at=datetime.utcnow())
        await self.history_repo.add_message(session_id, msg)

    def _default_user(self) -> UserProfile:
        return UserProfile(username="User", bio="")

    def _default_waifu(self) -> WaifuPersona:
        return WaifuPersona(name="Waifu", system_instruction="You are a helpful assistant.")