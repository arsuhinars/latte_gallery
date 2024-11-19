from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from latte_gallery.accounts.repository import AccountRepository
from latte_gallery.core.schemas import Page
from latte_gallery.pictures.models import Picture
from latte_gallery.pictures.repositories import PictureRepository
from latte_gallery.pictures.schemas import PictureCreateSchema, PictureUpdateSchema


class PictureService:
    def __init__(
        self, repository: PictureRepository, account_repository: AccountRepository
    ):
        self._repository = repository
        self._account_repository = account_repository

    async def create(
        self, owner_id: int, schema: PictureCreateSchema, session: AsyncSession
    ) -> Picture:
        owner = await self._account_repository.find_by_id(owner_id, session)
        if owner is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        picture = Picture(**schema.model_dump(), owner=owner)

        session.add(picture)
        await session.commit()

        return picture

    async def find_by_id(self, id: int, session: AsyncSession) -> Picture:
        picture = await self._repository.find_by_id(id, session)
        if picture is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return picture

    async def find_all(
        self,
        owner_id: int | None,
        title: str | None,
        page: int,
        size: int,
        session: AsyncSession,
    ) -> Page[Picture]:
        count = await self._repository.count_all(owner_id, title, session)
        pictures = await self._repository.find_all(
            owner_id, title, page * size, size, session
        )
        return Page(count=count, items=pictures)

    async def update_by_id(
        self, id: int, schema: PictureUpdateSchema, session: AsyncSession
    ) -> Picture:
        picture = await self._repository.find_by_id(id, session)
        if picture is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        for k, v in schema.model_dump().items():
            setattr(picture, k, v)

        await session.commit()

        return picture
