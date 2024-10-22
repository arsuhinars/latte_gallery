from fastapi import APIRouter, status

from latte_gallery.schemas import (
    AccountRegisterSchema,
    AccountSchema,
    Role,
    StatusResponse,
)

status_router = APIRouter(prefix="/status")
accounts_router = APIRouter(prefix="/accounts", tags=["Аккаунты"])


@status_router.get("", summary="Получить статус сервера", tags=["Статус"])
def get_status() -> StatusResponse:
    return StatusResponse(status="ok")


@accounts_router.post(
    "/register",
    summary="Регистрация нового аккаунта",
    status_code=status.HTTP_201_CREATED,
)
def register_account(body: AccountRegisterSchema) -> AccountSchema:
    return AccountSchema(
        id=1,
        login=body.login,
        name=body.name,
        role=Role.USER,
    )


@accounts_router.get("/my", summary="Получение данных своего аккаунта")
def get_my_account() -> AccountSchema:
    return AccountSchema(
        id=1,
        login="user1",
        name="Вася Пупкин",
        role=Role.USER,
    )
