import logging
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from app.domain.interfaces.services.embedder import IEmbedder

logger = logging.getLogger(__name__)

class QdrantInitializer:
    def __init__(
        self, 
        client: AsyncQdrantClient, 
        embedder: IEmbedder,
        collection_name: str
    ):
        self.client = client
        self.embedder = embedder
        self.collection_name = collection_name

    async def run(self):
        if await self.client.collection_exists(self.collection_name):
            return

        logger.info(f"Initializing Qdrant collection: '{self.collection_name}'")

        try:
            dummy_vec = await self.embedder.get_vector("warmup")
            size = len(dummy_vec)
            logger.info(f"Detected vector size: {size}")
        except Exception as e:
            logger.error(f"Embedder error: {e}")
            raise

        await self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=size,
                distance=models.Distance.COSINE
            )
        )
        logger.info("Collection created!")