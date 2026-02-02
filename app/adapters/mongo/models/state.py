from typing import Optional
from beanie import Document
from app.adapters.mongo.models.base import AuditMixin

class AppStateDoc(Document, AuditMixin):
    """
    Persists UI state so the user returns to exactly where they left off.
    """
    last_active_persona_id: Optional[str] = None
    last_active_session_id: Optional[str] = None
    
    ui_theme: str = "dracula"
    ui_font_size: int = 12

    class Settings:
        name = "app_state"