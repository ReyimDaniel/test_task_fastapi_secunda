from http.client import HTTPException

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.db_helper import db_helper
from app.repositories import activity_repository
from app.schemas.activity import ActivityRead, ActivityUpdate, ActivityCreate

router = APIRouter(tags=['activity'])


@router.get('/all_activities', response_model=list[ActivityRead],
            summary="Получить список всех деятельностей из базы данных",
            description="Эндпоинт для получения списка всех деятельностей из базы данных.")
async def read_all_activities(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await activity_repository.get_all_activities(session=session)


@router.get('/activity/{activity_id}', response_model=ActivityRead,
            summary="Получить деятельность из базы данных по ID",
            description="Эндпоинт для получения конкретной деятельности из базы данных по её ID.")
async def get_activity_by_id(activity_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    activity = await activity_repository.get_activity_by_id(session=session, activity_id=activity_id)
    if activity is not None:
        return activity
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Деятельность с ID {activity_id} не найдена!")


@router.post('/', response_model=ActivityRead,
             status_code=status.HTTP_201_CREATED,
             summary="Добавить новую деятельность в базу данных",
             description="Эндпоинт для добавления новой деятельности в базу данных.")
async def create_activity(activity_in: ActivityCreate,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await activity_repository.create_activity(session=session, activity_in=activity_in)


@router.put('/{activity_id}', response_model=ActivityRead,
            summary="Обновить все данные по деятельности",
            description="Эндпоинт для обновления данных по деятельности.")
async def update_activity(activity_id: int, activity_update: ActivityUpdate,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    activity = await activity_repository.get_activity_by_id(session=session, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found!")
    return await activity_repository.update_activity(session=session, activity=activity,
                                                     activity_update=activity_update)


@router.patch('/{activity_id}', response_model=ActivityRead,
              summary="Обновить некоторые данные по деятельности",
              description="Эндпоинт для частичного обновления данных по деятельности.")
async def update_activity_partial(activity_id: int, activity_update: ActivityUpdate,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    activity = await activity_repository.get_activity_by_id(session=session, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found!")
    return await activity_repository.update_activity(session=session, activity=activity,
                                                     activity_update=activity_update, partial=True)


@router.delete('/{activity_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить деятельность из базы данных",
               description="Эндпоинт для удаления деятельности. "
                           "Необходимо ввести ID деятельности, которую необходимо удалить из базы данных.")
async def delete_activity(activity_id: int,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    activity = await activity_repository.get_activity_by_id(session=session, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found!")
    await activity_repository.delete_activity(session=session, activity=activity)
