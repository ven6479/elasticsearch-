from app.config.settings import (
    DB_FILE
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_URL = f"sqlite+aiosqlite:///./{DB_FILE}"
SQLALCHEMY_URL_MIGRATIONS = f"sqlite:///./{DB_FILE}"

engine = create_async_engine(SQLALCHEMY_URL)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
