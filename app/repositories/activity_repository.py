from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models import Activity
from app.schemas.activity import ActivityUpdate, ActivityCreate


async def get_all_activities(session: AsyncSession):
    result = await session.execute(select(Activity).order_by(Activity.id))
    return result.scalars().all()


async def get_activity_by_id(session: AsyncSession, activity_id: int):
    try:
        result = await session.execute(select(Activity).where(Activity.id == activity_id))
        activity = result.scalar_one_or_none()
        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Activity with id {activity_id} not found"
            )
        return activity
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Ошибка при получении деятельности {activity_id}: {str(e)}")


async def create_activity(session: AsyncSession, activity_in: ActivityCreate) -> Activity:
    try:
        db_activity = Activity(
            name=activity_in.name,
            parent_id=activity_in.parent_id,
        )
        session.add(db_activity)
        await session.commit()
        await session.refresh(db_activity)
        return db_activity
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def update_activity(session: AsyncSession, activity: Activity, activity_update: ActivityUpdate,
                          partial: bool = False):
    try:
        for key, value in activity_update.model_dump(exclude_unset=partial).items():
            setattr(activity, key, value)
        await session.commit()
        await session.refresh(activity)
        return activity
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_activity(session: AsyncSession, activity: Activity):
    try:
        await session.delete(activity)
        await session.commit()
        return {"detail": "Activity deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
