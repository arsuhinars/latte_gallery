from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from latte_gallery.accounts.routers import accounts_router
from latte_gallery.core.routers import status_router
from latte_gallery.security.dependencies import authorize_user


def create_app():
    app = FastAPI(
        title="LatteGallery",
        dependencies=[Depends(authorize_user)],
    )

    app.include_router(status_router)
    app.include_router(accounts_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
    )

    return app
