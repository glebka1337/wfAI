from dataclasses import asdict
from datetime import datetime
from typing import Any, List
from uuid import uuid4
from qdrant_client import AsyncQdrantClient
from qdrant_client import models
from app.domain.entities.memory import MemoryFragment
from app.domain.interfaces.repositories.memory import IMemoryRepository
from app.domain.interfaces.services.embedder import IEmbedder
import logging

logger = logging.getLogger(__name__)

class QdrantMemoryRepository(IMemoryRepository):
    
    def __init__(
        self,
        client: AsyncQdrantClient,
        embedder: IEmbedder,
        collection_name: str = 'memory'
    ) -> None:
        self.client = client
        self.collection_name = collection_name
        self.embedder = embedder
    
    async def add_fragment(self, fragment: MemoryFragment) -> str:
        vector = await self.embedder.get_vector(fragment.content)
        point_id = fragment.vector_id or str(uuid4())
        
        raw_payload = asdict(fragment)
        payload = self._clean_payload(raw_payload)
        
        await self.client.upsert(
            collection_name=self.collection_name,
            points=[models.PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            )]
        )
        
        return point_id

    async def search_relevant(
        self,
        query: str, 
        limit: int = 3,
        threshold: float = 0.7
    ) -> List[MemoryFragment]:
        
        vec = await self.embedder.get_vector(query)
        
        search_result = await self.client.query_points(
            collection_name=self.collection_name,
            query=vec,  
            limit=limit,
            score_threshold=threshold,
            with_payload=True
        )
        
        memories = []
        for res in search_result.points:
            if not res.payload: 
                continue

            try:
                res.payload['vector_id'] = str(res.id)                
                memories.append(MemoryFragment(**res.payload))
            
            except TypeError as e: 
                logger.error(f'Failed to deserialize memory {res.id}: {e}')
                continue
    
        return memories
    
    async def delete_fragment(self, vector_id: str) -> None:
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=[vector_id]
            )
        )
        logger.info(f"Deleted memory: {vector_id}")
    
    def _clean_payload(
        self,
        payload: dict
    ) -> dict:
        """
        Cleans payload for future use
        """
        out = {}
        for k, v in payload.items():
            if v is None:
                continue
            if isinstance(v, datetime):
               out[k] = v.isoformat()
            else:
                out[k] = v
        return out