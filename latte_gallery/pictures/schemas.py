from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


class PictureSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    creation_date_time: datetime
    is_private: bool
    owner_id: int


class PictureCreateSchema(BaseModel):
    title: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
    ]
    is_private: bool


class PictureUpdateSchema(BaseModel):
    title: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
    ]
    is_private: bool
