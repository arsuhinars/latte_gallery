import typing
from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from latte_gallery.core.db import Base

if typing.TYPE_CHECKING:
    from latte_gallery.accounts.models import Account


class Picture(Base):
    __tablename__ = "pictures"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    creation_date_time: Mapped[datetime] = mapped_column(server_default=func.now())
    is_private: Mapped[bool]
    owner_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))

    owner: Mapped["Account"] = relationship(back_populates="pictures")
