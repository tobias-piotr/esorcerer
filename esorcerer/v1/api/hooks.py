import uuid
from dataclasses import asdict

from fastapi import APIRouter, Body, Depends, Path, status

from esorcerer.domain import models, services
from esorcerer.v1.dependencies import get_hook_service
from esorcerer.v1.models import HookFiltersModel, OrderingModel, PaginationModel
from esorcerer.v1.utils import dict_factory

router = APIRouter(tags=["hooks"], prefix="/hooks")


@router.post(
    "/",
    response_model=models.HookModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_hook(
    body: models.HookCreateModel = Body(...),
    service: services.HookService = Depends(get_hook_service),
) -> models.HookModel:
    """Create a new hook."""
    return await service.create(body)


@router.get(
    "/{uid}",
    response_model=models.HookModel,
    status_code=status.HTTP_200_OK,
)
async def get_hook(
    uid: uuid.UUID,
    service: services.HookService = Depends(get_hook_service),
) -> models.HookModel:
    """Get hook by id."""
    return await service.get(uid)


@router.get(
    "/",
    response_model=list[models.HookModel],
    status_code=status.HTTP_200_OK,
)
async def get_hooks(
    filters: HookFiltersModel = Depends(),
    ordering: OrderingModel = Depends(),
    pagination: PaginationModel = Depends(),
    service: services.HookService = Depends(get_hook_service),
) -> list[models.HookModel]:
    """Get hooks."""
    return await service.collect(
        filters=asdict(filters, dict_factory=dict_factory) or None,
        ordering=[ordering.order_by.value] if ordering.order_by else None,
        pagination=asdict(pagination) or None,
    )


@router.patch(
    "/{uid}",
    response_model=models.HookModel,
    status_code=status.HTTP_200_OK,
)
async def update_hook(
    uid: uuid.UUID = Path(...),
    body: models.HookUpdateModel = Body(...),
    service: services.HookService = Depends(get_hook_service),
):
    """Update hook."""
    return await service.update(uid, body)


@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hook(
    uid: uuid.UUID,
    service: services.HookService = Depends(get_hook_service),
) -> None:
    """Delete hook."""
    return await service.delete(uid)
