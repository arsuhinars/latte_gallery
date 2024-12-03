from contextlib import asynccontextmanager
from typing import cast

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from latte_gallery.accounts.repository import AccountRepository
from latte_gallery.accounts.routers import accounts_router
from latte_gallery.accounts.services import AccountsCreator, AccountService
from latte_gallery.core.db import DatabaseManager
from latte_gallery.core.routers import status_router
from latte_gallery.core.settings import AppSettings
from latte_gallery.pictures.repositories import PictureRepository
from latte_gallery.pictures.routers import pictures_router
from latte_gallery.pictures.services import PictureService
from latte_gallery.security.dependencies import authenticate_user


def create_app():
    settings = AppSettings()

    app = FastAPI(
        title="LatteGallery",
        dependencies=[Depends(authenticate_user)],
        lifespan=_app_lifespan,
        root_path_in_servers=False,
    )

    app.include_router(status_router)
    app.include_router(accounts_router)
    app.include_router(pictures_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
    )

    app.state.settings = settings
    app.state.db_manager = DatabaseManager(settings.db_url)

    account_repository = AccountRepository()
    picture_repository = PictureRepository()

    app.state.account_service = AccountService(account_repository)
    app.state.accounts_creator = AccountsCreator(
        settings.initial_accounts, account_repository, app.state.db_manager
    )
    app.state.picture_service = PictureService(picture_repository, account_repository)

    return app


@asynccontextmanager
async def _app_lifespan(app: FastAPI):
    db_manager = cast(DatabaseManager, app.state.db_manager)
    accounts_creator = cast(AccountsCreator, app.state.accounts_creator)

    await db_manager.initialize()
    await accounts_creator.initialize()
    yield
    await accounts_creator.dispose()
    await db_manager.dispose()
