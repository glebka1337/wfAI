import logging
from typing import List, Optional
from datetime import datetime
from app.domain.entities.chat import DialogSession, DialogSessionSummary, Message
from app.domain.interfaces.repositories.chat import IChatRepository
from app.domain.exceptions import SessionNotFound
from app.adapters.mongo.models.chat import DialogSessionDoc, ChatMessageDoc

logger = logging.getLogger(__name__)

INITIAL_LOAD_SIZE = 30 

class MongoChatRepository(IChatRepository):
    """
    Implementation of Chat Persistence using MongoDB.

    Manages both Sessions and Messages as a single Aggregate to ensure consistency.
    """

    async def create_session(self, session: DialogSession) -> None:
        """
        Creates a new session metadata record. 
        Messages are empty at creation.
        """
        doc = DialogSessionDoc.from_entity(session)
        await doc.insert()
        logger.info(f"Created new session: {session.uid}")

    async def get_session(self, uid: str) -> Optional[DialogSession]:
        """
        Retrieves Session Metadata + Initial Context (last N messages).
        Does NOT load the full history (OOM protection).
        """
        # 1. Fetch Metadata
        doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == uid)
        if not doc:
            return None
            
        # 2. Fetch Initial Context (Tail of the chat)
        # Sort DESC (Newest first) -> Limit -> Fetch
        msg_docs = await ChatMessageDoc.find(
            ChatMessageDoc.session_id == uid
        ).sort("-created_at").limit(INITIAL_LOAD_SIZE).to_list()
        
        # 3. Construct Entity
        # DB returns: [Today, Yesterday, Last Week]
        # Domain needs: [Last Week, Yesterday, Today] (Chronological)
        messages = [m.to_entity() for m in reversed(msg_docs)]
        
        entity = doc.to_entity() 
        entity.messages = messages 
        
        return entity

    async def get_history(
        self, 
        session_id: str, 
        limit: int = 20, 
        older_than: Optional[datetime] = None # <--- ЧЕЛОВЕЧЕСКИЙ НЕЙМИНГ
    ) -> List[Message]:
        """
        Infinite Scroll: Загрузка истории вверх.
        """
        query = (ChatMessageDoc.session_id == session_id)
    
        if older_than:
            query = query & (ChatMessageDoc.created_at < older_than)

        docs = await ChatMessageDoc.find(query)\
            .sort("-created_at")\
            .limit(limit)\
            .to_list()
        
        return [doc.to_entity() for doc in reversed(docs)]

    async def list_sessions(self, limit: int = 20, offset: int = 0) -> List[DialogSessionSummary]:
        """
        Optimized list for sidebars.
        Returns LIGHTWEIGHT summaries (no messages loaded).
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
        Updates metadata (title, status, updated_at).
        """
        doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == session.uid)
        
        if not doc:
            logger.warning(f"Update failed: Session {session.uid} not found")
            raise SessionNotFound(f"Session {session.uid} not found")
        
        doc.title = session.title
        doc.status = session.status.value
        doc.updated_at = session.updated_at
        # doc.persona_id = session.persona_id  # Uncomment if hot-swap needed
        
        await doc.save()

    async def delete_session(self, uid: str) -> None:
        """
        Manual Cascade Delete.
        1. Delete all messages for this session.
        2. Delete the session document.
        """
        session_doc = await DialogSessionDoc.find_one(DialogSessionDoc.uid == uid)
        
        if session_doc:
            # 1. Delete all messages linked to this session
            delete_result = await ChatMessageDoc.find(
                ChatMessageDoc.session_id == uid
            ).delete()
            
            # 2. Delete the session itself
            await session_doc.delete()
            
            # Defensive check
            deleted_count = delete_result.deleted_count if delete_result else 0
            
            logger.info(f"Deleted session {uid} and {deleted_count} messages.")
        else:
            logger.info(f"Delete skipped: Session {uid} not found")

    async def add_message(self, session_id: str, message: Message) -> None:
        """
        Saves a message AND updates the session's timestamp.
        """
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
        Retrieves the context window for the LLM (Short-term memory).
        """
        # 1. Fetch N newest messages
        docs = await ChatMessageDoc.find(
            ChatMessageDoc.session_id == session_id
        ).sort("-created_at").limit(limit).to_list()
        
        # 2. Reverse to chronological order (Old -> New)
        # LLM reads from top to bottom
        entities = [doc.to_entity() for doc in docs]
        return list(reversed(entities))