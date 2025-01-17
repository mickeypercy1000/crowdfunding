from fastapi import APIRouter
from app.api.v1.authentication import router as auth_router


routers = APIRouter()
# router_list = [docvec_router, videokyc_router]
router_list = [auth_router]

for router in router_list:
    routers.include_router(router)


