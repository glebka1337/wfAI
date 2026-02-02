import logging
from typing import List, Optional
from datetime import datetime
from app.core.config import settings
from app.domain.entities.chat import DialogSession, DialogSessionSummary, Message
from app.domain.interfaces.repositories.chat import IChatRepository
from app.domain.exceptions import SessionNotFound
from app.adapters.mongo.models.chat import DialogSessionDoc, ChatMessageDoc

logger = logging.getLogger(__name__)

class MongoChatRepository(IChatRepository):
    """
    Implementation of Chat Persistence using MongoDB.
    """

    async def create_session(self, session: DialogSession) -> None:
        doc = DialogSessionDoc.from_entity(session)
        await doc.insert()
        logger.info(f"Created new session: {session.uid}")

    async def get_session(self, uid: str) -> Optional[DialogSession]:
        # 1. Fetch Metadata
        doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == uid)
        if not doc:
            return None
            
        # 2. Fetch Initial Context (Tail of the chat)
        msg_docs = await ChatMessageDoc.find(
            ChatMessageDoc.session_id == uid
        ).sort("-created_at").limit(settings.INITIAL_LOAD_SIZE).to_list()
        
        # 3. Construct Entity (Reverse to chronological: Old -> New)
        messages = [m.to_entity() for m in reversed(msg_docs)]
        
        entity = doc.to_entity() 
        entity.messages = messages 
        
        return entity

    async def get_history(
        self, 
        session_id: str, 
        limit: int = 20, 
        older_than: Optional[datetime] = None
    ) -> List[Message]:
        """
        Cursor Pagination for Infinite Scroll.
        """
        query = (ChatMessageDoc.session_id == session_id)
        
        if older_than:
            query = query & (ChatMessageDoc.created_at < older_than)

        # Fetch from DB (Newest to Oldest relative to cursor)
        docs = await ChatMessageDoc.find(query)\
            .sort("-created_at")\
            .limit(limit)\
            .to_list()
            
        # Return in chronological order (Oldest -> Newest)
        return [doc.to_entity() for doc in reversed(docs)]

    async def list_sessions(self, limit: int = 20, offset: int = 0) -> List[DialogSessionSummary]:
        docs = await DialogSessionDoc.find_all()\
            .sort("-updated_at")\
            .skip(offset)\
            .limit(limit)\
            .to_list()
            
        return [doc.to_summary() for doc in docs]
    
    async def update_session(self, session: DialogSessionSummary) -> None:
        doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == session.uid)
        
        if not doc:
            raise SessionNotFound(f"Session {session.uid} not found")
        
        doc.title = session.title
        doc.status = session.status.value
        doc.updated_at = session.updated_at
        
        await doc.save()

    async def delete_session(self, uid: str) -> None:
        session_doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == uid)
        
        if session_doc:
            # 1. Delete messages
            delete_result = await ChatMessageDoc.find(
                ChatMessageDoc.session_id == uid
            ).delete()
            
            # 2. Delete session
            await session_doc.delete()
            
            count = delete_result.deleted_count if delete_result else 0
            logger.info(f"Deleted session {uid} and {count} messages.")

    async def add_message(self, session_id: str, message: Message) -> None:
        # 1. Save message
        msg_doc = ChatMessageDoc.from_entity(message, session_id=session_id)
        await msg_doc.insert()
        
        # 2. Update parent session timestamp
        session_doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == session_id)
        if session_doc:
            session_doc.updated_at = message.created_at
            await session_doc.save()

    async def get_last_messages(self, session_id: str, limit: int = 10) -> List[Message]:
        docs = await ChatMessageDoc.find(
            ChatMessageDoc.session_id == session_id
        ).sort("-created_at").limit(limit).to_list()
        
        # Reverse for LLM Context (Old -> New)
        entities = [doc.to_entity() for doc in docs]
        return list(reversed(entities))