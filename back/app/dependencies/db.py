from typing import Annotated

from app.config.db import async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


GetDb = Annotated[AsyncSession, Depends(get_db)]
