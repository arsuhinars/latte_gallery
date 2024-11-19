from typing import Annotated, Generic, Literal, TypeVar

from annotated_types import Le
from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveInt

PageNumber = NonNegativeInt
PageSize = Annotated[PositiveInt, Le(100)]


class StatusResponse(BaseModel):
    status: Literal["ok"]


ItemT = TypeVar("ItemT")


class Page(BaseModel, Generic[ItemT]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    count: int
    items: list[ItemT]
