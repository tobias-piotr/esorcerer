import uuid
from dataclasses import asdict

from fastapi import APIRouter, Body, Depends, status

from esorcerer.domain import models, services
from esorcerer.v1.dependencies import get_event_service
from esorcerer.v1.models import EventFiltersModel, OrderingModel, PaginationModel
from esorcerer.v1.utils import dict_factory

router = APIRouter(tags=["events"], prefix="/events")


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
    filters: EventFiltersModel = Depends(),
    ordering: OrderingModel = Depends(),
    pagination: PaginationModel = Depends(),
    service: services.EventService = Depends(get_event_service),
) -> list[models.EventModel]:
    """Get events."""
    return await service.collect(
        filters=asdict(filters, dict_factory=dict_factory) or None,
        ordering=[ordering.order_by.value] if ordering.order_by else None,
        pagination=asdict(pagination) or None,
    )


@router.get(
    "/project/{entity_id}",
    response_model=models.ProjectionModel,
    status_code=status.HTTP_200_OK,
)
async def project(
    entity_id: uuid.UUID,
    service: services.EventService = Depends(get_event_service),
) -> models.ProjectionModel:
    """Create projection for given entity."""
    return await service.project(entity_id)
