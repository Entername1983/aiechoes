from pydantic import BaseModel

from app.schemas.config import config


class RepliesSchema(BaseModel):
    model_config = config
    id: int
    time_created: str
    model: str
    version: str
    reply: str
    batch_id: int
    number_in_batch: int
    story_id: int


class ImagesSchema(BaseModel):
    model_config = config
    id: int
    batch_id: int
    title: str
    image_url: str
    thumbnail_url: str
    img_model: str
    time_created: str
    story_id: int


class SimpleImagesSchema(BaseModel):
    model_config = config
    id: int
    url: str


class PreSignedUrlResponse(BaseModel):
    model_config = config
    images_list: list[SimpleImagesSchema]


class RepliesResponse(BaseModel):
    model_config = config
    replies_list: list[RepliesSchema]
    has_more_next: bool
    has_more_prev: bool


class StoriesSchema(BaseModel):
    model_config = config
    id: int
    title: str
    live: bool
    story_type: str


class StoryContextsSchema(BaseModel):
    model_config = config
    id: int
    story_id: int
    context: dict
