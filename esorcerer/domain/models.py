import datetime
import uuid

from pydantic import BaseModel


class EventModel(BaseModel):
    """Event model."""

    id: uuid.UUID
    created_at: datetime.datetime
    type: str
    entity_id: uuid.UUID | None
    payload: dict


class EventCreateModel(BaseModel):
    """Model for event creation."""

    type: str
    entity_id: uuid.UUID | None = None
    payload: dict
