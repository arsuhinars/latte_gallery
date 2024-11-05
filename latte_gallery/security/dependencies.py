from typing import Annotated

from fastapi import Depends
from fastapi.security.http import HTTPBasic, HTTPBasicCredentials

from latte_gallery.accounts.models import Account
from latte_gallery.core.dependencies import AccountServiceDep, SessionDep

SecuritySchema = HTTPBasic(auto_error=False)


async def authorize_user(
    credentials: Annotated[HTTPBasicCredentials | None, Depends(SecuritySchema)],
    account_service: AccountServiceDep,
    session: SessionDep,
):
    if credentials is None:
        return None

    return await account_service.authorize(
        credentials.username, credentials.password, session
    )


AuthorizedUser = Annotated[Account | None, Depends(authorize_user)]
