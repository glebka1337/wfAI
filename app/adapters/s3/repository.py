import boto3
from typing import List
from app.domain.interfaces.repositories.icons import IWaifuIconRepository

class S3WaifuIconRepository(IWaifuIconRepository):
    def __init__(self, s3_client, bucket_name: str, endpoint_url: str):
        self.s3 = s3_client
        self.bucket = bucket_name
        # For MinIO running in Docker, the endpoint internal URL is http://minio:9000
        # But for the frontend/browser to access it, we likely need localhost if not using a proxy.
        # However, the Repository just returns the path/key or full URL.
        # Let's return relative path or full URL based on Public access.
        # Since we set "public" policy, we can construct the URL.
        # Use endpoint_url from config which might be localhost for external access, 
        # or we might need a separate PUBLIC_URL config. 
        # For now, let's assume endpoint_url is accessible by browser (e.g. localhost:9000)
        self.endpoint_url = endpoint_url

    async def upload_icon(self, filename: str, content: bytes, content_type: str) -> str:
        self.s3.put_object(
            Bucket=self.bucket,
            Key=filename,
            Body=content,
            ContentType=content_type
        )
        return f"{self.endpoint_url}/{self.bucket}/{filename}"

    async def list_icons(self) -> List[str]:
        response = self.s3.list_objects_v2(Bucket=self.bucket)
        if 'Contents' not in response:
            return []
        
        return [
            f"{self.endpoint_url}/{self.bucket}/{obj['Key']}"
            for obj in response['Contents']
        ]

    async def delete_icon(self, filename: str) -> None:
        self.s3.delete_object(Bucket=self.bucket, Key=filename)
