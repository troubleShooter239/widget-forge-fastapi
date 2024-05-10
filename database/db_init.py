from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from database.models import Base
from utils.config import DB_CONNECTION

engine = create_async_engine(DB_CONNECTION)

session = async_sessionmaker(engine)

async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = session()
    try:
        yield db
    finally:
        await db.close()