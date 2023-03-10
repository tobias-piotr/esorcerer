from fastapi import FastAPI

from esorcerer.bootstrap import bootstrap
from esorcerer.internal.endpoints import router as internal_router
from esorcerer.settings import settings
from esorcerer.v1.api.router import router as v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"{settings.API_PREFIX}/api/docs",
    openapi_url=f"{settings.API_PREFIX}/api/openapi.json",
)

app = bootstrap(app)

app.include_router(internal_router, prefix=settings.API_PREFIX)
app.include_router(v1_router, prefix=settings.API_PREFIX)
