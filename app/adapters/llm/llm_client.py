from typing import Any, AsyncGenerator, Dict, List, Optional
import openai
from openai import AsyncOpenAI  
import logging
from app.domain.entities.chat import Message, MessageRole
from app.domain.interfaces.llm import ILLMClient

logger = logging.getLogger(__name__)

class OpenAIClient(ILLMClient):
    
    def __init__(
        self,
        base_url: str,
        api_key: str = 'ollama', 
        model: str = "llama3"
    ):

        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            max_retries=3
        )
        self.default_model = model
    
    def _to_openai_format( 
        self,
        sys_prompt: str,
        messages: List[Message]
    ) -> List[dict]:
        
        payload = []
        
        if sys_prompt:
            payload.append({
                "role": "system",
                "content": sys_prompt
            })
        
        for msg in messages:
            if msg.role == MessageRole.ASSISTANT:
                role_str = "assistant"
            elif msg.role == MessageRole.SYSTEM:
                role_str = "system"
            else:
                role_str = "user"

            payload.append({
                "role": role_str,
                "content": msg.content
            })
            
        return payload
        
    async def stream_chat(
        self, 
        messages: List[Message], 
        system_instruction: str,
        model: Optional[str] = None, 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        
        target_model = model or self.default_model
        
        openai_messages = self._to_openai_format(
            sys_prompt=system_instruction, 
            messages=messages
        )

        request_params: Dict[str, Any] = {
            "model": target_model,
            "messages": openai_messages,
            "temperature": temperature,
            "stream": True, 
            **kwargs 
        }
        
        if max_tokens is not None:
            request_params["max_tokens"] = max_tokens

        try:
            stream = await self.client.chat.completions.create(**request_params)

            async for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield delta.content

        except openai.APIConnectionError:
            logger.critical("Connection Error: Is Ollama running at correct URL?")
            yield "[System Error: LLM Provider Unreachable]"
            
        except Exception as e:
            logger.exception("LLM Client Error")
            yield f"[System Error: {str(e)}]"