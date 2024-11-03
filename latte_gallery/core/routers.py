from fastapi import APIRouter
from latte_gallery.core.schemas import StatusResponse

status_router = APIRouter(prefix="/status")


@status_router.get("", summary="Получить статус сервера", tags=["Статус"])
def get_status() -> StatusResponse:
    return StatusResponse(status="ok")
