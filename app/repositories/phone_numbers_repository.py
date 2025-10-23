from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models import PhoneNumber
from app.schemas.phone_numbers import PhoneNumberCreate, PhoneNumberUpdate


async def get_all_phone_numbers(session: AsyncSession):
    result = await session.execute(select(PhoneNumber).order_by(PhoneNumber.id))
    return result.scalars().all()


async def get_phone_number_by_id(session: AsyncSession, phone_number_id: int):
    phone_number = await session.execute(select(PhoneNumber).where(PhoneNumber.id == phone_number_id))
    if not phone_number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Phone number with id {phone_number_id} not found",
        )
    return phone_number


async def create_phone_number(session: AsyncSession, phone_number_in: PhoneNumberCreate) -> PhoneNumber:
    try:
        db_phone_number = PhoneNumber(
            number=phone_number_in.number,
            organization_id=phone_number_in.organization_id,
        )
        session.add(db_phone_number)
        await session.commit()
        await session.refresh(db_phone_number)
        return db_phone_number
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def update_phone_number(session: AsyncSession, phone_number: PhoneNumber,
                              phone_number_update: PhoneNumberUpdate, partial: bool = False):
    try:
        for key, value in phone_number_update.model_dump(exclude_unset=partial).items():
            setattr(phone_number, key, value)
        await session.commit()
        await session.refresh(phone_number)
        return phone_number
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_phone_number(session: AsyncSession, phone_number: PhoneNumber):
    try:
        await session.delete(phone_number)
        await session.commit()
        return {"detail": "Phone number deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
