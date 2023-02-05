from fastapi import APIRouter

from esorcerer.v1.api.events import router as events_router
from esorcerer.v1.api.hooks import router as hooks_router

router = APIRouter(tags=["v1"], prefix="/api/v1")

router.include_router(events_router)
router.include_router(hooks_router)
