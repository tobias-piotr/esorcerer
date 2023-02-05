import uuid
from dataclasses import dataclass

from fastapi import Query

from esorcerer.v1 import types


@dataclass
class OrderingModel:
    """Ordering model."""

    order_by: types.OrderingField | None = Query(None)


@dataclass
class PaginationModel:
    """Pagination model."""

    page: int = Query(0)
    per_page: int = Query(10)


@dataclass
class EventFiltersModel:
    """Event filters model."""

    type: str | None = Query(None)
    entity_id: uuid.UUID | None = Query(None)


@dataclass
class HookFiltersModel:
    """Hook filters model."""

    is_active: bool | None = Query(None)
