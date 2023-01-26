import uuid

from esorcerer.domain import models
from esorcerer.plugins.database import models as db_models


class EventDBRepository:
    """Event database repository."""

    async def create(self, data: dict) -> models.EventModel:
        """Create a new event."""
        event = await db_models.EventModel.create(**data)
        return models.EventModel.from_orm(event)

    async def get(self, uid: uuid.UUID) -> models.EventModel:
        """Get event by id."""
        event = await db_models.EventModel.get(id=uid)
        return models.EventModel.from_orm(event)

    async def collect(self) -> list[models.EventModel]:
        """Get events by parameters."""
        events = await db_models.EventModel.all()
        return [models.EventModel.from_orm(event) for event in events]
