import uvicorn
from fastapi import FastAPI

from app.controllers.organization_controller import router as organization_router
from app.controllers.activity_controller import router as activity_router
from app.controllers.building_controller import router as building_router
from app.controllers.phone_numbers_controller import router as phone_numbers_router

app = FastAPI(title="Secunda API")
app.include_router(organization_router, prefix="/organizations")
app.include_router(activity_router, prefix="/activities")
app.include_router(building_router, prefix="/buildings")
app.include_router(phone_numbers_router, prefix="/phone_numbers")


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)