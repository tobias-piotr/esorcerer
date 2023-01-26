import uuid
from dataclasses import dataclass

from fastapi import Query

from esorcerer.v1 import types


@dataclass
class EventFiltersModel:
    """Event filters model."""

    type: str | None = Query(None)
    entity_id: uuid.UUID | None = Query(None)


@dataclass
class EventOrderingModel:
    """Event ordering model."""

    order_by: types.EventOrderingField | None = Query(None)


@dataclass
class PaginationModel:
    """Pagination model."""

    page: int = Query(0)
    per_page: int = Query(10)
