import uuid

from fastapi import APIRouter, Body, Depends, status

from esorcerer.domain import models, services
from esorcerer.v1.dependencies import get_event_service

router = APIRouter(tags=["v1"], prefix="/api/v1/events")


@router.post(
    "/",
    response_model=models.EventModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    body: models.EventCreateModel = Body(...),
    service: services.EventService = Depends(get_event_service),
) -> models.EventModel:
    """Create a new event."""
    return await service.create(body)


@router.get(
    "/{uid}",
    response_model=models.EventModel,
    status_code=status.HTTP_200_OK,
)
async def get_event(
    uid: uuid.UUID,
    service: services.EventService = Depends(get_event_service),
) -> models.EventModel:
    """Get event by id."""
    return await service.get(uid)


@router.get(
    "/",
    response_model=list[models.EventModel],
    status_code=status.HTTP_200_OK,
)
async def get_events(
    service: services.EventService = Depends(get_event_service),
) -> list[models.EventModel]:
    """Get events."""
    return await service.collect()
