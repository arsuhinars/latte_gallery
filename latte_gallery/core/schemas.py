from typing import Annotated, Generic, Literal, TypeVar

from annotated_types import Le
from pydantic import BaseModel, NonNegativeInt, PositiveInt

PageNumber = NonNegativeInt
PageSize = Annotated[PositiveInt, Le(100)]


class StatusResponse(BaseModel):
    status: Literal["ok"]


ItemT = TypeVar("ItemT")


class Page(BaseModel, Generic[ItemT]):
    count: int
    items: list[ItemT]
