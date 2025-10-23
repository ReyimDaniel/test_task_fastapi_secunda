import math

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models import Building
from app.schemas.building import BuildingUpdate, BuildingCreate


async def get_all_buildings(session: AsyncSession):
    result = await session.execute(select(Building).order_by(Building.id))
    return result.scalars().all()


async def get_building_by_id(session: AsyncSession, building_id: int) -> Building:
    try:
        result = await session.execute(select(Building).where(Building.id == building_id))
        building = result.scalar_one_or_none()
        if not building:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Building with id {building_id} not found",
            )
        return building
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Ошибка при получении здания {building_id}: {str(e)}")


async def create_building(session: AsyncSession, building_in: BuildingCreate) -> Building:
    try:
        db_building = Building(
            address=building_in.address,
            latitude=building_in.latitude,
            longitude=building_in.longitude,
        )
        session.add(db_building)
        await session.commit()
        await session.refresh(db_building)
        return db_building
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def update_building(session: AsyncSession, building: Building,
                          building_update: BuildingUpdate, partial: bool = False):
    try:
        for key, value in building_update.model_dump(exclude_unset=partial).items():
            setattr(building, key, value)
        await session.commit()
        await session.refresh(building)
        return building
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_building(session: AsyncSession, building: Building):
    try:
        await session.delete(building)
        await session.commit()
        return {"detail": "Building deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_buildings_in_bounds(
        session: AsyncSession,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
):
    result = await session.execute(
        select(Building).where(Building.latitude.between(lat_min, lat_max),
                               Building.longitude.between(lon_min, lon_max)).order_by(Building.id))
    return result.scalars().all()


# TODO
EARTH_RADIUS_KM = 6371.0


def haversine_distance(latitude1, longitude1, latitude2, longitude2):
    lat1, lon1, lat2, lon2 = map(math.radians, [latitude1, longitude1, latitude2, longitude2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return EARTH_RADIUS_KM * c


async def get_buildings_in_radius(session: AsyncSession,
                                  center_lat: float, center_lon: float, radius_km: float):
    result = await session.execute(select(Building))
    buildings = result.scalars().all()
    nearby_buildings = [b for b in buildings
                        if haversine_distance(center_lat, center_lon, b.latitude, b.longitude) <= radius_km]
    return nearby_buildings
