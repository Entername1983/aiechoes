from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import async_session


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


GetDb = Annotated[AsyncSession, Depends(get_db)]
