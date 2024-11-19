import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class DatabaseManager:
    def __init__(self, db_url: str):
        self._db_url = db_url

    async def initialize(self):
        from latte_gallery.accounts.models import Account  # noqa: F401
        from latte_gallery.pictures.models import Picture  # noqa: F401

        self._engine = create_async_engine(self._db_url)
        self._session_maker = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )
        async with self._engine.begin() as connect:
            logger.info("Database was initialized")
            await connect.run_sync(Base.metadata.create_all)

    async def dispose(self):
        logger.info("Database was disposed")
        await self._engine.dispose()

    @asynccontextmanager
    async def get_session(self):
        async with self._session_maker() as session:
            try:
                yield session
            finally:
                await session.rollback()
