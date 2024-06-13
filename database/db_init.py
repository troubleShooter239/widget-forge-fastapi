from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from database.models import Base
from utils.settings import settings

engine = create_async_engine(settings.db_connection_string)

session = async_sessionmaker(engine)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = session()
    try:
        yield db
    finally:
        await db.close()

db_dependency = Annotated[AsyncSession, Depends(get_db)]