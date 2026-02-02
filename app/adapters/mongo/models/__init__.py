from .user import UserProfileDoc
from .persona import WaifuPersonaDoc
from .chat import DialogSessionDoc, ChatMessageDoc
from .memory import MemoryFragmentDoc
from .state import AppStateDoc

ALL_DOCUMENT_MODELS = [
    UserProfileDoc,
    WaifuPersonaDoc,
    DialogSessionDoc,
    ChatMessageDoc,
    MemoryFragmentDoc,
    AppStateDoc
]