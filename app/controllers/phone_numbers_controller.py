from http.client import HTTPException

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.db_helper import db_helper
from app.repositories import phone_numbers_repository
from app.schemas.phone_numbers import PhoneNumberRead, PhoneNumberUpdate, PhoneNumberCreate

router = APIRouter(tags=['phone_numbers'])


@router.get('/all_phone_numbers', response_model=list[PhoneNumberRead],
            summary="Получить список всех номеров телефона из базы данных",
            description="Эндпоинт для получения списка всех номеров телефона из базы данных.")
async def get_all_phone_numbers(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await phone_numbers_repository.get_all_phone_numbers(session=session)


@router.get('/phone_numbers/{phone_number_id}', response_model=PhoneNumberRead,
            summary="Получить номер телефона из базы данных по ID",
            description="Эндпоинт для получения конкретного номера телефона из базы данных по ID.")
async def get_phone_number_by_id(phone_number_id: int,
                                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    phone_number = await phone_numbers_repository.get_phone_number_by_id(session=session,
                                                                         phone_number_id=phone_number_id)
    if phone_number is not None:
        return phone_number
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Номер телефона с ID {phone_number_id} не найден!")


@router.post('/', response_model=PhoneNumberRead,
             status_code=status.HTTP_201_CREATED,
             summary="Добавить новый номер телефона в базу данных",
             description="Эндпоинт для добавление нового номера телефона в базу данных.")
async def create_phone_number(phone_number_in: PhoneNumberCreate,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await phone_numbers_repository.create_phone_number(session=session, phone_number_in=phone_number_in)


@router.put('/{phone_number_id},', response_model=PhoneNumberRead,
            summary="Обновить все данные по номеру телефона",
            description="Эндпоинт для обновления данных по номеру телефона.")
async def update_phone_number(phone_number_id: int, phone_number_update: PhoneNumberUpdate,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    phone_number = await phone_numbers_repository.get_phone_number_by_id(session=session,
                                                                         phone_number_id=phone_number_id)
    if not phone_number:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phone number not found!")
    return await phone_numbers_repository.update_phone_number(session=session, phone_number=phone_number,
                                                              phone_number_update=phone_number_update)


@router.patch('/{phone_number_id},', response_model=PhoneNumberRead,
              summary="Обновить некоторые данные по номеру телефона",
              description="Эндпоинт для частичного обновления данных по номеру телефона.")
async def update_phone_number(phone_number_id: int, phone_number_update: PhoneNumberUpdate,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    phone_number = await phone_numbers_repository.get_phone_number_by_id(session=session,
                                                                         phone_number_id=phone_number_id)
    if not phone_number:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phone number not found!")
    return await phone_numbers_repository.update_phone_number(session=session, phone_number=phone_number,
                                                              phone_number_update=phone_number_update, partial=True)


@router.delete('/{phone_number_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить номер телефона из базы данных",
               description="Эндпоинт для удаления номера телефона. "
                           "Необходимо ввести ID номера телефона, который необходимо удалить из базы данных.")
async def delete_phone_number(phone_number_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    phone_number = await phone_numbers_repository.get_phone_number_by_id(session=session,
                                                                         phone_number_id=phone_number_id)
    if not phone_number:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phone number not found!")
    await phone_numbers_repository.delete_phone_number(session=session, phone_number=phone_number)
