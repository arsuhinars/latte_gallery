from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from latte_gallery.accounts.models import Account


class AccountRepository:
    def __init__(self):
        pass

    async def find_by_id(self, id: int, session: AsyncSession) -> Account | None:
        return await session.get(Account, id)

    async def find_by_login(self, login: str, session: AsyncSession) -> Account | None:
        q = select(Account).where(Account.login == login)
        s = await session.execute(q)
        return s.scalar_one_or_none()

    async def count_all(self, session: AsyncSession) -> int:
        q = select(func.count()).select_from(Account)
        s = await session.execute(q)
        return s.scalar_one()

    async def find_all(
        self, offset: int, limit: int, session: AsyncSession
    ) -> list[Account]:
        q = select(Account).offset(offset).limit(limit).order_by(Account.id)
        s = await session.execute(q)
        return list(s.scalars().all())
