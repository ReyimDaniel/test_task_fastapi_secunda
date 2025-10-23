from pydantic import BaseModel


class BuildingBase(BaseModel):
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class BuildingCreate(BuildingBase):
    pass


class BuildingRead(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True


class BuildingUpdate(BaseModel):
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
