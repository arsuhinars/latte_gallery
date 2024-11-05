from typing import cast

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from latte_gallery.accounts.routers import accounts_router
from latte_gallery.core.db import DatabaseManager
from latte_gallery.core.routers import status_router
from latte_gallery.core.settings import AppSettings
from latte_gallery.security.dependencies import authorize_user


def create_app():
    settings = AppSettings()

    app = FastAPI(
        title="LatteGallery",
        dependencies=[Depends(authorize_user)],
        lifespan=_app_lifespan,
    )

    app.include_router(status_router)
    app.include_router(accounts_router)

    app.state.settings = settings
    app.state.db_manager = DatabaseManager(settings.db_url)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
    )

    return app


async def _app_lifespan(app: FastAPI):
    db_manager = cast(DatabaseManager, app.state.db_manager)

    await db_manager.initialize()
    yield
    await db_manager.dispose()
