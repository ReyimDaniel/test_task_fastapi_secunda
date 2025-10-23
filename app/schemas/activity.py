from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str
    parent_id: int | None = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None


class ActivityRead(BaseModel):
    id: int
    name: str
    parent_id: int | None

    class Config:
        from_attributes = True

