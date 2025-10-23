from pydantic import BaseModel


class PhoneNumberBase(BaseModel):
    number: str | None = None
    organization_id: int | None = None


class PhoneNumberCreate(PhoneNumberBase):
    pass


class PhoneNumberRead(BaseModel):
    id: int
    number: str
    organization_id: int

    class Config:
        from_attributes = True


class PhoneNumberUpdate(BaseModel):
    number: str | None = None
    organization_id: int | None = None
