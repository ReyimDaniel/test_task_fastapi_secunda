from pydantic import BaseModel

from app.schemas.activity import ActivityRead


class OrganizationBase(BaseModel):
    name: str | None = None
    building_id: int | None = None
    activity_ids: list[int] | None = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationRead(BaseModel):
    id: int
    name: str
    building_id: int
    activities: list[ActivityRead] | None = None

    class Config:
        from_attributes = True


class OrganizationUpdate(BaseModel):
    name: str | None = None
    building_id: int | None = None
    activity_id: int | None = None
