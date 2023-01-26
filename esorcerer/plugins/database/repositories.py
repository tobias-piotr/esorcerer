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

    async def collect(
        self,
        filters: dict | None = None,
        ordering: list[str] | None = None,
        pagination: dict | None = None,
    ) -> list[models.EventModel]:
        """Get events by parameters."""
        if filters is None:
            events = db_models.EventModel.all()
        else:
            events = db_models.EventModel.filter(**filters)

        if ordering is not None:
            events = events.order_by(*ordering)

        if pagination is not None:
            events = events.limit(pagination["per_page"]).offset(
                pagination["per_page"] * pagination["page"]
            )

        return [models.EventModel.from_orm(event) for event in await events]
