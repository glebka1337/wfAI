from dishka import Provider, Scope, provide

from app.core.config import Settings
from app.domain.interfaces.llm import ILLMClient
from app.domain.interfaces.repositories.chat import IChatRepository
from app.domain.interfaces.repositories.memory import IMemoryRepository
from app.domain.interfaces.repositories.user import IUserProfileRepository
from app.domain.interfaces.repositories.user import IUserProfileRepository
from app.domain.interfaces.repositories.persona import IPersonaRepository
from app.domain.interfaces.repositories.icons import IWaifuIconRepository
from app.application.commands.registry import CommandRegistry

# Chat UseCases
from app.application.usecases.chat.process_message import ProcessMessageUseCase
from app.application.usecases.chat.get_history import GetChatHistoryUseCase

# Session UseCases
from app.application.usecases.session.list_sessions import ListSessionsUseCase
from app.application.usecases.session.create_session import CreateSessionUseCase
from app.application.usecases.session.delete_session import DeleteSessionUseCase
from app.application.usecases.session.update_session import UpdateSessionTitleUseCase

# Settings UseCases
from app.application.usecases.settings.get_user_profile import GetUserProfileUseCase
from app.application.usecases.settings.update_user_profile import UpdateUserProfileUseCase
from app.application.usecases.settings.get_persona import GetWaifuPersonaUseCase
from app.application.usecases.settings.get_persona import GetWaifuPersonaUseCase
from app.application.usecases.settings.update_persona import UpdateWaifuPersonaUseCase
from app.application.usecases.settings.set_persona_icon import SetPersonaIconUseCase

# Command UseCases
from app.application.usecases.commands.list_commands import ListCommandsUseCase

# Icon UseCases
from app.application.usecases.icons.upload_icon import UploadIconUseCase
from app.application.usecases.icons.list_icons import ListIconsUseCase
from app.application.usecases.icons.delete_icon import DeleteIconUseCase


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_process_message_use_case(
        self,
        registry: CommandRegistry,
        memory_repo: IMemoryRepository,
        chat_repo: IChatRepository,
        user_repo: IUserProfileRepository,
        persona_repo: IPersonaRepository,
        llm_client: ILLMClient
    ) -> ProcessMessageUseCase:
        return ProcessMessageUseCase(
            registry=registry,
            memory_repo=memory_repo,
            history_repo=chat_repo,
            user_repo=user_repo,
            persona_repo=persona_repo,
            llm_client=llm_client
        )

    @provide
    def provide_get_chat_history_use_case(self, chat_repo: IChatRepository) -> GetChatHistoryUseCase:
        return GetChatHistoryUseCase(chat_repo)

    @provide
    def provide_list_sessions_use_case(self, chat_repo: IChatRepository) -> ListSessionsUseCase:
        return ListSessionsUseCase(chat_repo)

    @provide
    def provide_create_session_use_case(self, chat_repo: IChatRepository) -> CreateSessionUseCase:
        return CreateSessionUseCase(chat_repo)

    @provide
    def provide_delete_session_use_case(self, chat_repo: IChatRepository) -> DeleteSessionUseCase:
        return DeleteSessionUseCase(chat_repo)

    @provide
    def provide_update_session_title_use_case(self, chat_repo: IChatRepository) -> UpdateSessionTitleUseCase:
        return UpdateSessionTitleUseCase(chat_repo)

    @provide
    def provide_get_user_profile_use_case(self, user_repo: IUserProfileRepository) -> GetUserProfileUseCase:
        return GetUserProfileUseCase(user_repo)

    @provide
    def provide_update_user_profile_use_case(self, user_repo: IUserProfileRepository) -> UpdateUserProfileUseCase:
        return UpdateUserProfileUseCase(user_repo)

    @provide
    def provide_get_waifu_persona_use_case(self, persona_repo: IPersonaRepository) -> GetWaifuPersonaUseCase:
        return GetWaifuPersonaUseCase(persona_repo)

    @provide
    def provide_update_waifu_persona_use_case(self, persona_repo: IPersonaRepository) -> UpdateWaifuPersonaUseCase:
        return UpdateWaifuPersonaUseCase(persona_repo)

    @provide
    def provide_set_persona_icon_use_case(self, persona_repo: IPersonaRepository, settings: Settings) -> SetPersonaIconUseCase:
        return SetPersonaIconUseCase(persona_repo, settings)

    @provide
    def provide_list_commands_use_case(self, registry: CommandRegistry) -> ListCommandsUseCase:
        return ListCommandsUseCase(registry)

    @provide
    def provide_upload_icon_use_case(self, repo: IWaifuIconRepository) -> UploadIconUseCase:
        return UploadIconUseCase(repo)

    @provide
    def provide_list_icons_use_case(self, repo: IWaifuIconRepository) -> ListIconsUseCase:
        return ListIconsUseCase(repo)

    @provide
    def provide_delete_icon_use_case(self, repo: IWaifuIconRepository) -> DeleteIconUseCase:
        return DeleteIconUseCase(repo)