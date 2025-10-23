from sqlalchemy import Table, Column, ForeignKey, Integer
from app.models import Base

organization_activity = Table(
    "organization_activity",
    Base.metadata, Column("organization_id", ForeignKey("organization.id"), primary_key=True),
    Column("activity_id", ForeignKey("activity.id"), primary_key=True),
)
