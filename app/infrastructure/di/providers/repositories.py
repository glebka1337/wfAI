from dishka import Provider, Scope, provide
from qdrant_client import AsyncQdrantClient
from app.core.config import Settings
from app.domain.interfaces.services.embedder import IEmbedder
from app.domain.interfaces.repositories.chat import IChatRepository
from app.domain.interfaces.repositories.memory import IMemoryRepository
from app.domain.interfaces.repositories.user import IUserProfileRepository
from app.domain.interfaces.repositories.persona import IPersonaRepository
from app.adapters.mongo.repositories.chat import MongoChatRepository
from app.adapters.mongo.repositories.user import MongoUserProfileRepository
from app.adapters.mongo.repositories.persona import MongoPersonaRepository
from app.adapters.qdrant.memory_repository import QdrantMemoryRepository
from app.adapters.qdrant.initializer import QdrantInitializer

class RepositoriesProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_user_repo(self) -> IUserProfileRepository:
        return MongoUserProfileRepository()

    @provide
    def provide_persona_repo(self) -> IPersonaRepository:
        return MongoPersonaRepository()

    @provide
    def provide_chat_repo(self) -> IChatRepository:
        return MongoChatRepository()

    @provide
    def provide_memory_repo(
        self,
        client: AsyncQdrantClient,
        embedder: IEmbedder,
        settings: Settings
    ) -> IMemoryRepository:
        return QdrantMemoryRepository(
            client=client,
            embedder=embedder,
            collection_name=settings.QDRANT_COLLECTION
        )

    @provide
    def provide_qdrant_initializer(
        self,
        client: AsyncQdrantClient,
        embedder: IEmbedder,
        settings: Settings
    ) -> QdrantInitializer:
        return QdrantInitializer(
            client=client,
            embedder=embedder,
            collection_name=settings.QDRANT_COLLECTION
        )