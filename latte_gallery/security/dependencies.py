from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security.http import HTTPBasic, HTTPBasicCredentials

from latte_gallery.accounts.schemas import AccountSchema, Role

SecuritySchema = HTTPBasic(auto_error=False)


def authorize_user(
    credentials: Annotated[HTTPBasicCredentials | None, Depends(SecuritySchema)],
):
    if credentials is None:
        return None

    if credentials.username != "admin" or credentials.password != "qwerty12":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return AccountSchema(
        id=1,
        login="admin",
        name="Иван Петров",
        role=Role.MAIN_ADMIN,
    )
