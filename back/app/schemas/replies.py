from pydantic import BaseModel

from app.schemas.config import config


class RepliesSchema(BaseModel):
    model_config = config
    id: int
    time_created: str
    model: str
    version: str
    reply: str


class RepliesResponse(BaseModel):
    model_config = config
    replies_list: list[RepliesSchema]
