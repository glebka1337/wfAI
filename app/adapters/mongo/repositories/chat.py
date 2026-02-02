import logging
from typing import List, Optional
from app.domain.entities.chat import DialogSession, DialogSessionSummary, Message
from app.domain.interfaces.repositories.chat import IChatRepository
from app.domain.exceptions import SessionNotFound
from app.adapters.mongo.models.chat import DialogSessionDoc, ChatMessageDoc

logger = logging.getLogger(__name__)

class MongoChatRepository(IChatRepository):
    """
    Implementation of Chat Persistence using MongoDB.
    
    Architecture Note:
    - Splits concept of 'Session Metadata' (SessionDoc) and 'Content' (MessageDoc).
    - Handles manual aggregation to build full Domain Entities.
    """

    async def create_session(self, session: DialogSession) -> None:
        """
        Persist a new session. 
        Note: We ignore session.messages here as a new session starts empty.
        """
        doc = DialogSessionDoc.from_entity(session)
        await doc.insert()
        logger.info(f"Created new session: {session.uid}")

    async def get_session(self, uid: str) -> Optional[DialogSession]:
        """
        Retrieves the FULL session aggregate.
        1. Fetches metadata.
        2. Fetches recent messages.
        3. Combines them into a DialogSession entity.
        """
        # 1. Fetch Metadata
        doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == uid)
        if not doc:
            return None
            
        # 2. Fetch recent context (Hydration)
        msg_docs = await ChatMessageDoc.find(
            ChatMessageDoc.session_id == uid
        ).sort("-created_at").limit(50).to_list()
        
        # 3. Construct the Full Entity
        # Convert docs to entities and Reverse (DB: Newest->Oldest | Domain: Oldest->Newest)
        messages = [m.to_entity() for m in reversed(msg_docs)]
        
        entity = doc.to_entity() 
        entity.messages = messages 
        
        return entity

    async def list_sessions(self, limit: int = 20, offset: int = 0) -> List[DialogSessionSummary]:
        """
        Optimized list for sidebars.
        Returns LIGHTWEIGHT summaries (no messages).
        """
        docs = await DialogSessionDoc.find_all()\
            .sort("-updated_at")\
            .skip(offset)\
            .limit(limit)\
            .to_list()
            
        # Use to_summary() to strictly return the lighter dataclass
        return [doc.to_summary() for doc in docs]
    
    async def update_session(self, session: DialogSessionSummary) -> None:
        """
        Updates metadata (title, status, etc).
        Works with both Summary and Full Session objects.
        """
        doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == session.uid)
        
        if not doc:
            logger.warning(f"Update failed: Session {session.uid} not found")
            raise SessionNotFound(f"Session {session.uid} not found")
        
        doc.title = session.title
        doc.status = session.status.value
        doc.updated_at = session.updated_at
        doc.persona_id = session.persona_id 
        
        await doc.save()

    async def delete_session(self, uid: str) -> None:
        """
        Manual Cascade Delete.
        Mongo doesn't support FK cascades, so we clean up messages first.
        """
        session_doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == uid)
        
        if session_doc:
            # 1. Delete all messages linked to this session
            delete_result = await ChatMessageDoc.find(
                ChatMessageDoc.session_id == uid
            ).delete()
            
            # 2. Delete the session itself
            await session_doc.delete()
            
            # Pylance Fix: defensive coding in case delete_result is None
            deleted_count = delete_result.deleted_count if delete_result else 0
            
            logger.info(f"Deleted session {uid} and {deleted_count} messages.")
        else:
            logger.info(f"Delete skipped: Session {uid} not found")

    async def add_message(self, session_id: str, message: Message) -> None:
        # 1. Save the message to the separate collection
        msg_doc = ChatMessageDoc.from_entity(message, session_id=session_id)
        await msg_doc.insert()
        
        # 2. Update the parent session's 'updated_at' field
        # This ensures the chat jumps to the top of the list in list_sessions()
        session_doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == session_id)
        if session_doc:
            session_doc.updated_at = message.created_at
            await session_doc.save()

    async def get_last_messages(self, session_id: str, limit: int = 10) -> List[Message]:
        """
        Retrieves the context window for the LLM.
        """
        # 1. Fetch N newest messages
        docs = await ChatMessageDoc.find(
            ChatMessageDoc.session_id == session_id
        ).sort("-created_at").limit(limit).to_list()
        
        # 2. Reverse to chronological order (Old -> New)
        entities = [doc.to_entity() for doc in docs]
        return list(reversed(entities))