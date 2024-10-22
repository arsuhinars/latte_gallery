from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from latte_gallery.routers import accounts_router, status_router


def create_app():
    app = FastAPI(title="LatteGallery")

    app.include_router(status_router)
    app.include_router(accounts_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
    )

    return app
