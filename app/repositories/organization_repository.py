import math
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from app.models import Organization, Activity, Building
from app.models.association_tables import organization_activity
from app.schemas.organization import OrganizationUpdate, OrganizationCreate, OrganizationRead


async def get_all_organizations(session: AsyncSession):
    result = await session.execute(
        select(Organization).options(selectinload(Organization.activities)).order_by(Organization.id))
    return result.scalars().all()


async def get_organization_by_id(session: AsyncSession, organization_id: int) -> Organization:
    try:
        result = await session.execute(select(Organization).options(selectinload(Organization.activities))
                                       .where(Organization.id == organization_id))
        organization = result.scalar_one_or_none()
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization with id {organization_id} not found"
            )
        return organization
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Ошибка при получении организации {organization_id}: {str(e)}")


async def get_organization_by_name(session: AsyncSession, organization_name: str) -> Organization:
    try:
        result = await session.execute(select(Organization).options(selectinload(Organization.activities)).where(
            Organization.name == organization_name))
        organization = result.scalar_one_or_none()
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization with name {organization_name} not found"
            )
        return organization
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Ошибка при получении организации {organization_name}: {str(e)}")


async def create_organization(session: AsyncSession, organization_in: OrganizationCreate):
    db_org = Organization(name=organization_in.name, building_id=organization_in.building_id)
    if organization_in.activity_ids:
        result = await session.execute(select(Activity).where(Activity.id.in_(organization_in.activity_ids)))
        db_org.activities = result.scalars().all()
    session.add(db_org)
    await session.commit()
    await session.refresh(db_org)
    await session.refresh(db_org, attribute_names=["activities"])
    return db_org


async def update_organization(session: AsyncSession, organization: Organization,
                              organization_update: OrganizationUpdate, partial: bool = False) -> Organization:
    try:
        for key, value in organization_update.model_dump(exclude_unset=partial).items():
            setattr(organization, key, value)
        await session.commit()
        await session.refresh(organization)
        return organization
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_organization(session: AsyncSession, organization: Organization):
    try:
        await session.delete(organization)
        await session.commit()
        return {"detail": "Organization deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# TODO
async def get_all_organization_located_in_building(session: AsyncSession, building_id: int):
    result = await session.execute(
        select(Organization).options(selectinload(Organization.activities)).where(
            Organization.building_id == building_id).order_by(Organization.id))
    return result.scalars().all()


async def get_descendants(session: AsyncSession, activity_id: int, visited=None) -> List[int]:
    if visited is None:
        visited = set()
    if activity_id in visited:
        return []
    visited.add(activity_id)

    descendants = [activity_id]
    result = await session.execute(select(Activity).where(Activity.parent_id == activity_id))
    children = result.scalars().all()
    for child in children:
        descendants.extend(await get_descendants(session, child.id, visited))
    return descendants


async def get_organizations_by_activity(session: AsyncSession, activity_id: int):
    try:
        result = await session.execute(select(Activity).where(Activity.id == activity_id))
        activity = result.scalar_one_or_none()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        all_activity_ids = await get_descendants(session, activity_id)
        result = await session.execute(
            select(Organization)
            .join(organization_activity, Organization.id == organization_activity.c.organization_id)
            .options(selectinload(Organization.activities))
            .where(organization_activity.c.activity_id.in_(all_activity_ids))
            .order_by(Organization.id))
        orgs = result.scalars().all()
        return [OrganizationRead.model_validate(o) for o in orgs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_organizations_in_bounds(
        session: AsyncSession,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float):
    result = await session.execute(
        select(Organization).join(Organization.building).options(selectinload(Organization.activities)).where(
            Building.latitude.between(lat_min, lat_max),
            Building.longitude.between(lon_min, lon_max)))
    return result.scalars().all()


EARTH_RADIUS_KM = 6371.0


def haversine_distance(latitude1, longitude1, latitude2, longitude2):
    lat1, lon1, lat2, lon2 = map(math.radians, [latitude1, longitude1, latitude2, longitude2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return EARTH_RADIUS_KM * c


async def get_organizations_in_radius(session: AsyncSession,
                                      center_lat: float, center_lon: float, radius_km: float, ):
    result = await session.execute(
        select(Organization).options(selectinload(Organization.building), selectinload(Organization.activities))
        .join(Organization.building))
    organizations = result.scalars().unique().all()
    nearby_orgs = [org for org in organizations
                   if org.building and haversine_distance(center_lat, center_lon, org.building.latitude,
                                                          org.building.longitude) <= radius_km]
    return nearby_orgs


async def get_descendants_limited(session: AsyncSession, activity_id: int, max_depth: int = 3) -> list[int]:
    descendants = [activity_id]
    current_level = [activity_id]

    for _ in range(max_depth):
        result = await session.execute(
            select(Activity.id).where(Activity.parent_id.in_(current_level))
        )
        next_level = [row[0] for row in result.all()]
        if not next_level:
            break
        descendants.extend(next_level)
        current_level = next_level

    return descendants


async def get_organizations_by_activity_limited(session: AsyncSession, activity_id: int, max_depth: int = 3):
    try:
        result = await session.execute(select(Activity).where(Activity.id == activity_id))
        activity = result.scalar_one_or_none()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        all_activity_ids = await get_descendants_limited(session, activity_id, max_depth=max_depth)
        result = await session.execute(
            select(Organization)
            .join(organization_activity, Organization.id == organization_activity.c.organization_id)
            .where(organization_activity.c.activity_id.in_(all_activity_ids))
            .options(selectinload(Organization.activities))
            .order_by(Organization.id))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
