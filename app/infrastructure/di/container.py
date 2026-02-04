from dishka import make_async_container, AsyncContainer
from app.infrastructure.di.providers.adapters import AdaptersProvider
from app.infrastructure.di.providers.repositories import RepositoriesProvider
from app.infrastructure.di.providers.usecases import UseCasesProvider
from app.infrastructure.di.providers.commands import CommandsProvider
from app.infrastructure.di.providers.s3 import S3Provider

def make_container() -> AsyncContainer:
    return make_async_container(
        AdaptersProvider(),
        RepositoriesProvider(),
        UseCasesProvider(),
        CommandsProvider(),
        S3Provider()
    )
