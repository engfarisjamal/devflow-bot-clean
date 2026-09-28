"""SQLAlchemy base and session."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from devflow_bot.config.settings import get_settings


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.app_debug,
    future=True,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with async_session_maker() as session:
        yield session
