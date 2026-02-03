from typing import List
from openai import AsyncOpenAI
from app.domain.interfaces.services.embedder import IEmbedder

class OpenAIEmbedder(IEmbedder):
    def __init__(
        self, 
        api_key: str, 
        base_url: str,
        model: str
    ):
        self.client = AsyncOpenAI(
            api_key=api_key, 
            base_url=base_url
        )
        self.model = model

    async def get_vector(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        response = await self.client.embeddings.create(
            input=[text], 
            model=self.model
        )
        return response.data[0].embedding