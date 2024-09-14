import mimetypes
from typing import Any, Union
from urllib.parse import urlparse

import aioboto3
from botocore.client import Config

from app.dependencies.settings import get_settings

settings = get_settings()


async_session = aioboto3.Session(
    aws_access_key_id=settings.s3.s3_access_key_id,
    aws_secret_access_key=settings.s3.s3_secret_access_key,
    config=Config(signature_version="s3v4"),
    region_name=settings.s3.s3_default_region,
)
async_s3_client = async_session.client("s3")
bucket = settings.s3.s3_bucket_name


class StorageManager:
    @staticmethod
    async def create_presigned_url(url: str, expiration: int = 3600) -> str | None:
        """Generate a presigned URL for a file in S3"""
        bucket, key = StorageManager.parse_s3_url(url)
        async with async_session.client("s3") as s3_client:
            return await s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expiration,
            )

    @staticmethod
    async def get_object(
        folder_name: str,
        object_name: str,
    ) -> Union[bool, Any]:  # noqa: ANN401
        object_key = f"{folder_name}/{object_name}"
        async with async_session.client("s3") as s3_client:
            return await s3_client.get_object(Bucket=bucket, Key=object_key)

    @staticmethod
    async def put_object(
        folder_name: str,
        file_name: str,
        object_name: str | None = None,
    ) -> bool:
        if object_name is None:
            object_name = file_name
        if folder_name:
            object_name = f"{folder_name}/{object_name}"
        content_type, _ = mimetypes.guess_type(object_name)
        async with async_session.client("s3") as s3_client:
            await s3_client.upload_file(
                file_name,
                bucket,
                object_name,
                ExtraArgs={"ContentType": content_type},
            )
        return True

    @staticmethod
    def parse_s3_url(url: str) -> tuple[str, str]:
        """Parse the S3 URL into bucket name and key.

        :param url: The full URL to an S3 object
        :return: bucket name and key
        """
        parsed_url = urlparse(url)
        # if not parsed_url.netloc.endswith("amazonaws.com"):
        #     msg = "URL does not belong to amazonaws.com"
        #     raise ValueError(msg)
        bucket_name = parsed_url.netloc.split(".")[0]
        key = parsed_url.path.lstrip("/")
        return bucket_name, key
