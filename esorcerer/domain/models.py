import datetime
import uuid

from pydantic import BaseModel, Field


class EventModel(BaseModel):
    """Event model."""

    id: uuid.UUID
    created_at: datetime.datetime
    type: str
    entity_id: uuid.UUID | None
    payload: dict

    class Config:
        orm_mode = True


class EventCreateModel(BaseModel):
    """Model for event creation."""

    type: str
    entity_id: uuid.UUID | None = None
    payload: dict = Field(default_factory=dict)
