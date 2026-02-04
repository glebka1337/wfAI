import boto3
from typing import Any
from dishka import Provider, Scope, provide
from app.core.config import Settings
from app.domain.interfaces.repositories.icons import IWaifuIconRepository
from app.adapters.s3.repository import S3WaifuIconRepository

class S3Provider(Provider):
    scope = Scope.APP

    @provide
    def provide_s3_client(self, settings: Settings) -> Any:
        return boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION_NAME
        )

    @provide
    def provide_icon_repo(self, client: Any, settings: Settings) -> IWaifuIconRepository:
        return S3WaifuIconRepository(
            s3_client=client,
            bucket_name=settings.S3_BUCKET_NAME,
            endpoint_url=settings.S3_PUBLIC_URL  # Use public URL for browser access
        )
