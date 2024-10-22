from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints


class StatusResponse(BaseModel):
    status: Literal["ok"]


class Role(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"
    MAIN_ADMIN = "MAIN_ADMIN"


class AccountSchema(BaseModel):
    id: int
    login: str
    name: str
    role: Role


PasswordStr = Annotated[
    str, StringConstraints(min_length=8, pattern=r"^[a-zA-Z0-9_-]+$")
]


class AccountRegisterSchema(BaseModel):
    login: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    password: PasswordStr
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
