from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import app_config

SQL_ALCHEMY_URL = (
    f"postgresql+asyncpg://{app_config.db_user}:{app_config.db_password}"
    f"@{app_config.db_host}:{app_config.db_port}/{app_config.db_name}"
)
engine = create_async_engine(SQL_ALCHEMY_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as db:
        yield db
