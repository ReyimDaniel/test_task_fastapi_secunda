from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
from app.models.association_tables import organization_activity

if TYPE_CHECKING:
    from app.models.organization import Organization


class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activity.id"))

    parent: Mapped["Activity"] = relationship(remote_side="Activity.id", back_populates="children")
    children: Mapped[list["Activity"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    organizations: Mapped[list["Organization"]] = relationship(secondary=organization_activity,
                                                               back_populates="activities")
