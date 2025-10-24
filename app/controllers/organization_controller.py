from http.client import HTTPException

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.db_helper import db_helper
from app.repositories import organization_repository
from app.schemas.organization import OrganizationRead, OrganizationCreate, OrganizationUpdate
from app.core.dependencies import verify_api_key

router = APIRouter(tags=['organizations'])


@router.get('/all_organizations', response_model=list[OrganizationRead],
            summary="Получить список всех организаций из базы данных",
            description="Эндпоинт для получения списка всех организаций из базы данных.")
async def read_all_organizations(session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                                 _: None = Depends(verify_api_key)):
    return await organization_repository.get_all_organizations(session=session)


@router.get('/organization/{organization_id}', response_model=OrganizationRead,
            summary="Получить организацию из базы данных по ID",
            description="Эндпоинт для получения конкретной организации из базы данных по её ID.")
async def get_organization_by_id(organization_id: int,
                                 session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                                 _: None = Depends(verify_api_key)):
    organization = await organization_repository.get_organization_by_id(session=session,
                                                                        organization_id=organization_id)
    if organization is not None:
        return organization
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Организация с ID {organization_id} не найдена!")


@router.post('/', response_model=OrganizationRead,
             status_code=status.HTTP_201_CREATED,
             summary="Добавить новую организацию в базу данных",
             description="Эндпоинт для добавления организации в базу данных.")
async def create_organization(organization_in: OrganizationCreate,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                              _: None = Depends(verify_api_key)):
    return await organization_repository.create_organization(session=session, organization_in=organization_in)


@router.put('/{organization_id}', response_model=OrganizationRead,
            summary="Обновить все данные по организации",
            description="Эндпоинт для обновления данных по организации.")
async def update_organization(organization_id: int, organization_update: OrganizationUpdate,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                              _: None = Depends(verify_api_key)):
    organization = await organization_repository.get_organization_by_id(session=session,
                                                                        organization_id=organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found!")
    return await organization_repository.update_organization(session=session, organization=organization,
                                                             organization_update=organization_update)


@router.patch('/{organization_id}', response_model=OrganizationRead,
              summary="Обновить некоторые данные по организации",
              description="Эндпоинт для частичного обновления данных по организации.")
async def update_organization_partial(organization_id: int, organization_update: OrganizationUpdate,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                                      _: None = Depends(verify_api_key)):
    organization = await organization_repository.get_organization_by_id(session=session,
                                                                        organization_id=organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found!")
    return await organization_repository.update_organization(session=session, organization=organization,
                                                             organization_update=organization_update, partial=True)


@router.delete('/{organization_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить организацию из базы данных",
               description="Эндпоинт для удаления организации. "
                           "Необходимо ввести ID организации, которую необходимо удалить из базы данных.")
async def delete_organization(organization_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                              _: None = Depends(verify_api_key)):
    organization = await organization_repository.get_organization_by_id(session=session,
                                                                        organization_id=organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found!")
    await organization_repository.delete_organization(session=session, organization=organization)
    return None


@router.get('/organization_in_building', response_model=list[OrganizationRead],
            summary="Получить список всех организаций из базы данных находящихся в здании.",
            description="Эндпоинт для получения списка всех "
                        "организаций из базы данных находящихся в конкретном здании.")
async def get_all_organization_located_in_building(building_id: int,
                                                   session: AsyncSession = Depends(
                                                       db_helper.scoped_session_dependency),
                                                   _: None = Depends(verify_api_key)):
    return await organization_repository.get_all_organization_located_in_building(session=session,
                                                                                  building_id=building_id)


@router.get('/organization_by_activity', response_model=list[OrganizationRead],
            summary="Получить список всех организаций из базы данных по виду деятельности.",
            description="Эндпоинт для получения списка всех "
                        "организаций из базы данных которые относятся к указанному виду деятельности.")
async def get_all_organization_by_activity(activity_id: int,
                                           session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                                           _: None = Depends(verify_api_key)):
    return await organization_repository.get_organizations_by_activity(session=session, activity_id=activity_id)


@router.get('/organization_in_bounds', response_model=list[OrganizationRead],
            summary="Получить список всех организаций из базы данных, "
                    "находящихся в выбранных координатах(Прямоугольная область).",
            description="Эндпоинт для получения списка всех "
                        "организаций из базы данных, находящихся в выбранных координатах широты и долготы. "
                        "Проверка по прямоугольной области.")
async def all_organizations_in_bounds(lat_min: float, lat_max: float, lon_min: float, lon_max: float,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                                      _: None = Depends(verify_api_key)):
    return await organization_repository.get_organizations_in_bounds(session, lat_min, lat_max, lon_min, lon_max)


@router.get('/organization_in_radius', response_model=list[OrganizationRead],
            summary="Получить список всех организаций из базы данных, "
                    "находящихся в выбранных координатах(Радиус).",
            description="Эндпоинт для получения списка всех "
                        "организаций из базы данных, находящихся в выбранных координатах широты и долготы. "
                        "Проверка по через радиус.")
async def all_organizations_in_radius(center_lat: float, center_lon: float, radius_km: float,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                                      _: None = Depends(verify_api_key)):
    return await organization_repository.get_organizations_in_radius(session=session, center_lat=center_lat,
                                                                     center_lon=center_lon,
                                                                     radius_km=radius_km)


@router.get("/organizations_by_activity_limited", response_model=list[OrganizationRead],
            summary="Получить организации по виду деятельности (до 3 уровней вложенности)",
            description="Возвращает организации указанной деятельности и её подкатегорий до 3 уровней.")
async def get_organizations_by_activity_limited_endpoint(activity_id: int,
                                                         session: AsyncSession = Depends(
                                                             db_helper.scoped_session_dependency),
                                                         _: None = Depends(verify_api_key)):
    return await organization_repository.get_organizations_by_activity_limited(session=session, activity_id=activity_id,
                                                                               max_depth=3)


@router.get('/organization_by_name/{organization_name}', response_model=OrganizationRead,
            summary="Получить организацию из базы данных по его названию",
            description="Эндпоинт для получения конкретной организации из базы данных по её названию.")
async def get_organization_by_name(organization_name: str,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                                   _: None = Depends(verify_api_key)):
    organization = await organization_repository.get_organization_by_name(session=session,
                                                                          organization_name=organization_name)
    if organization is not None:
        return organization
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Организация с названием {organization_name} не найдена!")
