from functools import lru_cache
from typing import Annotated

from app.config.settings import Settings
from fastapi import Depends


@lru_cache
def get_settings() -> Settings:
    return Settings()


AppSettings = Annotated[Settings, Depends(get_settings)]
