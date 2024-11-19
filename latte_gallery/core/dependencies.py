from typing import Annotated, cast

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from latte_gallery.accounts.services import AccountService
from latte_gallery.core.db import DatabaseManager
from latte_gallery.pictures.services import PictureService


async def session(request: Request):
    db_manager = cast(DatabaseManager, request.app.state.db_manager)
    async with db_manager.get_session() as session:
        yield session


def account_service(request: Request):
    return request.app.state.account_service


def picture_service(request: Request):
    return request.app.state.picture_service


SessionDep = Annotated[AsyncSession, Depends(session)]
AccountServiceDep = Annotated[AccountService, Depends(account_service)]
PictureServiceDep = Annotated[PictureService, Depends(picture_service)]
