from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from latte_gallery.accounts.models import Role


class AccountSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    name: str
    role: Role


LoginStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
PasswordStr = Annotated[
    str, StringConstraints(min_length=8, pattern=r"^[a-zA-Z0-9_-]+$")
]


class AccountCreateSchema(BaseModel):
    login: LoginStr
    password: PasswordStr
    name: NameStr
    role: Role


class AccountRegisterSchema(BaseModel):
    login: LoginStr
    password: PasswordStr
    name: NameStr


class AccountUpdateSchema(BaseModel):
    login: LoginStr
    name: NameStr
    role: Role


class AccountPasswordUpdateSchema(BaseModel):
    password: PasswordStr
