from typing import Optional

from app.schemas.config import config
from pydantic import BaseModel, Field


class RepliesSchema(BaseModel):
    model_config = config
    id: int
    time_created: str
    model: str
    reply: str


class RepliesResponse(BaseModel):
    model_config = config
    replies_list: list[RepliesSchema]
