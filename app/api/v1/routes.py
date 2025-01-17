from fastapi import APIRouter
from app.api.v1.authentication import router as auth_router
from app.api.v1.projects import router as project_router

routers = APIRouter()
router_list = [auth_router, project_router]

for router in router_list:
    routers.include_router(router)


