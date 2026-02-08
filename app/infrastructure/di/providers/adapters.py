from dishka import Provider, Scope, provide
from motor.motor_asyncio import AsyncIOMotorClient
from qdrant_client import AsyncQdrantClient
from app.core.config import Settings
from app.domain.interfaces.llm import ILLMClient
from app.domain.interfaces.tools.search import ISearchTool
from app.domain.interfaces.services.embedder import IEmbedder
from app.adapters.llm.llm_client import OpenAIClient
from app.adapters.llm.memory import OpenAIEmbedder 

class AdaptersProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_settings(self) -> Settings:
        return Settings()

    @provide
    def provide_mongo_client(self, settings: Settings) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(settings.MONGO_URL)

    @provide
    def provide_qdrant_client(self, settings: Settings) -> AsyncQdrantClient:
        return AsyncQdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )

    @provide
    def provide_llm_client(self, settings: Settings) -> ILLMClient:
        return OpenAIClient(
            base_url=settings.LLM_BASE_URL,
            api_key=settings.LLM_API_KEY,
            model=settings.DEFAULT_MODEL
        )

    @provide
    def provide_embedder(self, settings: Settings) -> IEmbedder:
        return OpenAIEmbedder(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            model=settings.EMBEDDING_MODEL 
        )

    @provide
    def provide_search_tool(self, settings: Settings) -> ISearchTool:
        from app.adapters.search.searxng import SearXNGSearchTool
        return SearXNGSearchTool()