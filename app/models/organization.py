from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
from app.models.association_tables import organization_activity

if TYPE_CHECKING:
    from app.models.activity import Activity
    from app.models.building import Building
    from app.models.phone_numbers import PhoneNumber


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    building_id: Mapped[int | None] = mapped_column(ForeignKey("building.id"))

    building: Mapped["Building"] = relationship(back_populates="organizations")
    activities: Mapped[list["Activity"]] = relationship(
        secondary=organization_activity, back_populates="organizations")
    phones: Mapped[list["PhoneNumber"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
