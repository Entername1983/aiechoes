# tests/test_storage_manager.py

from unittest.mock import AsyncMock, patch

import pytest

from app.s3.storage_manager import StorageManager

pytestmark = pytest.mark.asyncio



class TestStorageManager:
    
    @patch('app.s3.storage_manager.aioboto3.Session')
    async def test_put_object_success(self, mock_session):
        """Test successful upload of an object"""
        file_name = "batch_7_2024-09-16_09_28_30.956031_00_00.png"
        folder_name = "temp"
        file_path = "/path/to/test_image.png"
        object_name = None  # Should default to file name

        # Mock the S3 client and its put_object method
        mock_s3_client = AsyncMock()
        mock_s3_client.put_object.return_value = None  # put_object doesn't return anything
        mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client

        # Mock aiofiles.open to simulate reading file content
        with patch('app.s3.storage_manager.aiofiles.open', new_callable=AsyncMock) as mock_aiofiles_open, \
             patch('app.s3.storage_manager.Path') as mock_path:

            # Mock Path.name to return the filename
            mock_path.return_value.name = 'test_image.png'

            # Mock the file read
            mock_file = AsyncMock()
            mock_file.read.return_value = b'file content'
            mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

            # Call the method
            success = await StorageManager.put_object(folder_name, file_name)

            # Assertions
            assert success == True
            mock_s3_client.put_object.assert_called_once_with(
                Bucket='ai-images-1',
                Key='story_images/test_image.png',
                Body=b'file content',
                ContentType='image/png'
            )
            mock_aiofiles_open.assert_awaited_once_with(file_path, 'rb')
    
    
    # def test_parse_s3_url_valid(self):
    #     url = "http://ai-images-1.s3.amazonaws.com/story_images/test_image.png"
    #     bucket, key = StorageManager.parse_s3_url(url)
    #     assert bucket == "ai-images-1"
    #     assert key == "story_images/test_image.png"

    # def test_parse_s3_url_invalid(self):
    #     url = "http://invalidurl.com/test_image.png"
    #     bucket, key = StorageManager.parse_s3_url(url)
    #     assert bucket == "invalidurl"
    #     assert key == "test_image.png"

    # @pytest.mark.asyncio
    # async def test_create_presigned_url_success():
    #     url = "http://ai-images-1.s3.amazonaws.com/story_images/test_image.png"
    #     expiration = 600

    #     with patch("app.s3.storage_manager.aioboto3.Session") as mock_session:
    #         mock_s3_client = AsyncMock()
    #         mock_s3_client.generate_presigned_url.return_value = "http://presigned-url.com"
    #         mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client

    #         presigned_url = await StorageManager.create_presigned_url(url, expiration)
    #         assert presigned_url == "http://presigned-url.com"
    #         mock_s3_client.generate_presigned_url.assert_called_once_with(
    #             "get_object",
    #             Params={"Bucket": "ai-images-1", "Key": "story_images/test_image.png"},
    #             ExpiresIn=expiration,
    #         )

    # @pytest.mark.asyncio
    # async def test_create_presigned_url_failure():
    #     url = "http://ai-images-1.s3.amazonaws.com/story_images/test_image.png"
    #     expiration = 600

    #     with patch("app.s3.storage_manager.aioboto3.Session") as mock_session:
    #         mock_s3_client = AsyncMock()
    #         mock_s3_client.generate_presigned_url.side_effect = Exception("Failed to generate URL")
    #         mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client

    #         with pytest.raises(Exception) as exc_info:
    #             await StorageManager.create_presigned_url(url, expiration)
    #         assert "Failed to generate URL" in str(exc_info.value)

    

    # @patch('app.s3.storage_manager.aioboto3.Session')
    # async def test_get_object_success(self, mock_session):
    #     """Test successful retrieval of an object"""
    #     folder_name = "story_images"
    #     object_name = "test_image.png"

    #     # Mock the S3 client and its get_object method
    #     mock_s3_client = AsyncMock()
    #     mock_response = {
    #         'Body': AsyncMock()
    #     }
    #     mock_response['Body'].read.return_value = b'file content'
    #     mock_s3_client.get_object.return_value = mock_response
    #     mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client

    #     # Call the method
    #     result = await StorageManager.get_object(folder_name, object_name)

    #     # Assertions
    #     assert result == b'file content'
    #     mock_s3_client.get_object.assert_called_once_with(
    #         Bucket='ai-images-1',
    #         Key='story_images/test_image.png'
    #     )

    # @patch('app.s3.storage_manager.aioboto3.Session')
    # async def test_get_object_no_such_key(self, mock_session):
    #     """Test retrieval of a non-existent object"""
    #     folder_name = "story_images"
    #     object_name = "nonexistent_image.png"

    #     # Mock the S3 client to raise NoSuchKey exception
    #     mock_s3_client = AsyncMock()
    #     mock_s3_client.get_object.side_effect = mock_s3_client.exceptions.NoSuchKey
    #     mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client

    #     # Call the method
    #     result = await StorageManager.get_object(folder_name, object_name)

    #     # Assertions
    #     assert result == False
    #     mock_s3_client.get_object.assert_called_once_with(
    #         Bucket='ai-images-1',
    #         Key='story_images/nonexistent_image.png'
    #     )



    # @patch('app.s3.storage_manager.aioboto3.Session')
    # async def test_put_object_failure(self, mock_session):
    #     """Test failure during object upload"""
    #     folder_name = "story_images"
    #     file_path = "/path/to/test_image.png"
    #     object_name = "custom_name.png"

    #     # Mock the S3 client to raise an exception during put_object
    #     mock_s3_client = AsyncMock()
    #     mock_s3_client.put_object.side_effect = Exception("Upload failed")
    #     mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client

    #     # Mock aiofiles.open to simulate reading file content
    #     with patch('app.s3.storage_manager.aiofiles.open', new_callable=AsyncMock) as mock_aiofiles_open, \
    #          patch('app.s3.storage_manager.Path') as mock_path:

    #         # Mock Path.name to return the filename
    #         mock_path.return_value.name = 'test_image.png'

    #         # Mock the file read
    #         mock_file = AsyncMock()
    #         mock_file.read.return_value = b'file content'
    #         mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

    #         # Call the method
    #         success = await StorageManager.put_object(folder_name, file_path, object_name)

    #         # Assertions
    #         assert success == False
    #         mock_s3_client.put_object.assert_called_once_with(
    #             Bucket='ai-images-1',
    #             Key='story_images/custom_name.png',
    #             Body=b'file content',
    #             ContentType='image/png'
    #         )
    #         mock_aiofiles_open.assert_awaited_once_with(file_path, 'rb')