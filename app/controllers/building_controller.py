from http.client import HTTPException

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.db_helper import db_helper
from app.repositories import building_repository
from app.schemas.building import BuildingRead, BuildingUpdate, BuildingCreate
from app.core.dependencies import verify_api_key

router = APIRouter(tags=['building'])


@router.get("/all_buildings", response_model=list[BuildingRead],
            summary="Получить список всех зданий из базы данных",
            description="Эндпоинт для получения списка всех зданий из базы данных.")
async def get_all_buildings(session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                            _: None = Depends(verify_api_key)):
    return await building_repository.get_all_buildings(session=session)


@router.get("/building/{building_id}", response_model=BuildingRead,
            summary="Получить здание из базы данных по ID",
            description="Эндпоинт для получения конкретного здания из базы данных по ID.")
async def get_building_by_id(building_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                             _: None = Depends(verify_api_key)):
    building = await building_repository.get_building_by_id(session=session, building_id=building_id)
    if building is not None:
        return building
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Здание с ID {building_id} не найдено!")


@router.post("/", response_model=BuildingRead,
             status_code=status.HTTP_201_CREATED,
             summary="Добавить новое здание в базу данных",
             description="Эндпоинт для добавление нового здания в базу данных.")
async def create_building(building_in: BuildingCreate,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                          _: None = Depends(verify_api_key)):
    return await building_repository.create_building(session=session, building_in=building_in)


@router.put('/{building_id}', response_model=BuildingRead,
            summary="Обновить все данные по зданию",
            description="Эндпоинт для обновления данных по зданию.")
async def update_building(building_id: int, building_update: BuildingUpdate,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                          _: None = Depends(verify_api_key)):
    building = await building_repository.get_building_by_id(session=session, building_id=building_id)
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found!")
    return await building_repository.update_building(session=session, building=building,
                                                     building_update=building_update)


@router.patch('/{building_id}', response_model=BuildingRead,
              summary="Обновить некоторые данные по зданию",
              description="Эндпоинт для частичного обновления данных по зданию.")
async def update_building_partial(building_id: int, building_update: BuildingUpdate,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                                  _: None = Depends(verify_api_key)):
    building = await building_repository.get_building_by_id(building_id=building_id, session=session)
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found!")
    return await building_repository.update_building(session=session, building=building,
                                                     building_update=building_update, partial=True)


@router.delete('/{building_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить здание из базы данных",
               description="Эндпоинт для удаления здания. "
                           "Необходимо ввести ID здания, которое необходимо удалить из базы данных.")
async def delete_building(building_id: int,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                          _: None = Depends(verify_api_key)):
    building = await building_repository.get_building_by_id(session=session, building_id=building_id)
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found!")
    await building_repository.delete_building(session=session, building=building)


@router.get('/buildings_in_bounds', response_model=list[BuildingRead],
            summary="Получить список всех зданий из базы данных, "
                    "находящихся в выбранных координатах(Прямоугольная область).",
            description="Эндпоинт для получения списка всех "
                        "зданий из базы данных, находящихся в выбранных координатах широты и долготы. "
                        "Проверка по прямоугольной области.")
async def all_organizations_in_bounds(lat_min: float, lat_max: float, lon_min: float, lon_max: float,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                                      _: None = Depends(verify_api_key)):
    return await building_repository.get_buildings_in_bounds(session=session, lat_min=lat_min, lat_max=lat_max,
                                                             lon_min=lon_min, lon_max=lon_max)


@router.get('/buildings_in_radius', response_model=list[BuildingRead],
            summary="Получить список всех зданий из базы данных, "
                    "находящихся в выбранных координатах(Радиус).",
            description="Эндпоинт для получения списка всех "
                        "зданий из базы данных, находящихся в выбранных координатах широты и долготы. "
                        "Проверка по радиусу.")
async def all_organizations_in_radius(center_lat: float, center_lon: float, radius_km: float,
                                      session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                                      _: None = Depends(verify_api_key)):
    return await building_repository.get_buildings_in_radius(session=session, center_lat=center_lat,
                                                             center_lon=center_lon, radius_km=radius_km)
