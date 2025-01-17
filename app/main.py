from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.v1.routes import routers as v1_routers


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=True 
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_routers, prefix="/api/v1")
