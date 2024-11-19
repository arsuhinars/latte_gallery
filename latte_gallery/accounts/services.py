import logging

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from latte_gallery.accounts.models import Account
from latte_gallery.accounts.repository import AccountRepository
from latte_gallery.accounts.schemas import AccountCreateSchema, AccountUpdateSchema
from latte_gallery.core.db import DatabaseManager
from latte_gallery.core.schemas import Page

logger = logging.getLogger(__name__)


class AccountService:
    def __init__(self, repository: AccountRepository):
        self._repository = repository

    async def create(self, schema: AccountCreateSchema, session: AsyncSession):
        account = await self._repository.find_by_login(schema.login, session)
        if account is not None:
            raise HTTPException(status.HTTP_409_CONFLICT)

        account = Account(**schema.model_dump())

        session.add(account)
        await session.commit()

        return account

    async def authorize(self, login: str, password: str, session: AsyncSession):
        account = await self._repository.find_by_login(login, session)
        if account is None or account.password != password:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        return account

    async def find_by_id(self, id: int, session: AsyncSession):
        account = await self._repository.find_by_id(id, session)
        if account is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return account

    async def find_all(self, page: int, size: int, session: AsyncSession):
        count = await self._repository.count_all(session)
        users = await self._repository.find_all(page * size, size, session)
        return Page(count=count, items=users)

    async def update_by_id(
        self, id: int, schema: AccountUpdateSchema, session: AsyncSession
    ):
        account = await self._repository.find_by_id(id, session)
        if account is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        for k, v in schema.model_dump().items():
            setattr(account, k, v)

        await session.commit()

        return account

    async def update_password_by_id(
        self, id: int, password: str, session: AsyncSession
    ):
        account = await self._repository.find_by_id(id, session)
        if account is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        account.password = password

        await session.commit()

        return account


class AccountsCreator:
    def __init__(
        self,
        accounts: list[AccountCreateSchema],
        repository: AccountRepository,
        db_manager: DatabaseManager,
    ):
        self._accounts = accounts
        self._repository = repository
        self._db_manager = db_manager

    async def initialize(self):
        logger.info("Started creating initial accounts")
        async with self._db_manager.get_session() as session:
            for account in self._accounts:
                a = await self._repository.find_by_login(account.login, session)
                if a is not None:
                    logger.info(f"Account with login={account.login} already exists")
                    continue

                a = Account(**account.model_dump())
                session.add(a)

            await session.commit()
        logger.info("Finished creating initial accounts")

    async def dispose(self):
        pass
