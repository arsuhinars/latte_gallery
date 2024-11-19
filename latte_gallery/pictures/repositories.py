from sqlalchemy import ColumnExpressionArgument, and_, func, select, true
from sqlalchemy.ext.asyncio import AsyncSession

from latte_gallery.pictures.models import Picture


class PictureRepository:
    def __init__(self):
        pass

    async def find_by_id(self, id: int, session: AsyncSession) -> Picture | None:
        return await session.get(Picture, id)

    async def count_all(
        self, owner_id: int | None, title: str | None, session: AsyncSession
    ) -> int:
        q: list[ColumnExpressionArgument] = [true()]

        if owner_id is not None:
            q.append(Picture.owner_id == owner_id)

        if title is not None:
            q.append(func.lower(Picture.title).like(f"*{title.lower()}*"))

        s = await session.execute(
            select(func.count())
            .select_from(Picture)
            .where(and_(*q))
            .order_by(Picture.creation_date_time.desc()),
        )

        return s.scalar_one()

    async def find_all(
        self,
        owner_id: int | None,
        title: str | None,
        offset: int,
        limit: int,
        session: AsyncSession,
    ) -> list[Picture]:
        q: list[ColumnExpressionArgument] = [true()]

        if owner_id is not None:
            q.append(Picture.owner_id == owner_id)

        if title is not None:
            q.append(func.lower(Picture.title).like(f"*{title.lower()}*"))

        s = await session.execute(
            select(Picture)
            .where(and_(*q))
            .offset(offset)
            .limit(limit)
            .order_by(Picture.creation_date_time.desc()),
        )

        return list(s.scalars().all())
