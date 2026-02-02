from typing import Any, AsyncGenerator, Dict, List, Optional
import openai
from app.domain.entities.chat import Message, MessageRole
from app.domain.interfaces.llm import ILLMClient
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class OpenAIClient(ILLMClient):
    
    def __init__(
        self,
        base_url: str,
        api_key: str = 'ollama', # for local llm
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            max_retries=3
        )
    
    def _to_open_ai_forma(
        self,
        sys_prompt: str,
        messages: List[Message]
    ) -> List[dict]:
        
        payload = []
        
        if sys_prompt:
            payload.append(
                {
                    "role": "system",
                    "content": sys_prompt
                }
            )
        
        for msg in messages:
            role_str = "assistant" if msg.role == MessageRole.ASSISTANT else "user"
            payload.append({
                "role": role_str,
                "content": msg.content
            })
            
        return payload
        
    async def stream_chat(
        self, 
        messages: List[Message], 
        system_instruction: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        
        openai_messages = self._to_open_ai_forma(sys_prompt=system_instruction, messages=messages)

        request_params: Dict[str, Any] = {
            "model": model,
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
            logger.error("Connection Error: Is Ollama/LLM running?")
            yield "[System Error: LLM Provider Unreachable]"
            
        except openai.RateLimitError:
            logger.error("Rate limit exceeded")
            yield "[System Error: Rate Limit Exceeded]"
            
        except openai.APIStatusError as e:
            logger.error(f"API Error: {e.status_code} - {e.response}")
            yield f"[System Error: Provider returned {e.status_code}]"
        except Exception as e:
            logger.exception("Unexpected LLM Client Error")
            yield f"[System Error: {str(e)}]"