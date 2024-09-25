import logging
import mimetypes
from typing import Any, Union

import aioboto3
from botocore.client import Config

from app.dependencies.settings import get_settings

settings = get_settings()

# Set the log level for Boto3, Aiobotocore, and Botocore
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("aiobotocore").setLevel(logging.WARNING)
logging.getLogger("s3transfer").setLevel(logging.WARNING)

async_session = aioboto3.Session()
async_s3_client = async_session.client(
    "s3",
    endpoint_url=settings.s3.s3_public_endpoint,
    aws_access_key_id=settings.s3.s3_access_key_id,
    aws_secret_access_key=settings.s3.s3_secret_access_key,
    config=Config(signature_version="s3v4"),
    region_name=settings.s3.s3_default_region,
)
bucket = settings.s3.s3_bucket_name


class StorageManager:
    @staticmethod
    async def create_presigned_url(url: str, expiration: int = 3600) -> str | None:
        """Generate a presigned URL for a file in S3"""
        bucket, key = url.split("/", 1)
        async with async_session.client(
            "s3",
            endpoint_url=settings.s3.s3_public_endpoint,
            aws_access_key_id=settings.s3.s3_access_key_id,
            aws_secret_access_key=settings.s3.s3_secret_access_key,
            config=Config(signature_version="s3v4"),
            region_name=settings.s3.s3_default_region,
        ) as s3_client:  # type: ignore
            return await s3_client.generate_presigned_url(
                "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expiration
            )

    @staticmethod
    async def get_object(folder_name: str, object_name: str) -> Union[bool, Any]:  # noqa: ANN401
        object_key = f"{folder_name}/{object_name}"
        async with async_s3_client as s3_client:
            return await s3_client.get_object(Bucket=bucket, Key=object_key)

    @staticmethod
    async def upload_file_to_s3(file: bytes, bucket_name: str, object_name: str) -> None:
        async with async_session.client(
            "s3",
            endpoint_url=settings.s3.s3_internal_endpoint,
            aws_access_key_id=settings.s3.s3_access_key_id,
            aws_secret_access_key=settings.s3.s3_secret_access_key,
            config=Config(signature_version="s3v4"),
            region_name=settings.s3.s3_default_region,
        ) as async_s3_client:  # type: ignore
            await async_s3_client.put_object(
                Body=file,
                Bucket=bucket_name,
                Key=object_name,
                ContentType=mimetypes.guess_type(object_name)[0] or "application/octet-stream",
            )
