from fastapi import APIRouter

from latte_gallery.core.dependencies import SessionDep
from latte_gallery.core.schemas import StatusResponse

status_router = APIRouter(prefix="/status")


@status_router.get("", summary="Получить статус сервера", tags=["Статус"])
def get_status(session: SessionDep) -> StatusResponse:
    return StatusResponse(status="ok")
