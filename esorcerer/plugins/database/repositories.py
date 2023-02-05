import abc
import uuid
from typing import Generic, TypeVar

from pydantic import BaseModel
from tortoise import functions

from esorcerer.domain import exceptions, models
from esorcerer.plugins.database import models as db_models

DatabaseModel = TypeVar("DatabaseModel", bound=db_models.BaseModel)
DomainModel = TypeVar("DomainModel", bound=BaseModel)


class DBRepository(abc.ABC, Generic[DatabaseModel, DomainModel]):
    """Base repository handling basic database operations."""

    db_model: type[DatabaseModel]
    domain_model: type[DomainModel]

    async def create(self, data: dict) -> DomainModel:
        """Create a new entry."""
        entry = await self.db_model.create(**data)
        return self.domain_model.from_orm(entry)

    async def get(self, uid: uuid.UUID) -> DomainModel:
        """Get entry by id."""
        entry = await self.db_model.get_or_none(id=uid)
        if not entry:
            raise exceptions.NotFoundError()
        return self.domain_model.from_orm(entry)

    async def collect(
        self,
        filters: dict | None = None,
        ordering: list[str] | None = None,
        pagination: dict | None = None,
    ) -> list[DomainModel]:
        """Get entries by parameters."""
        if filters is None:
            entries = self.db_model.all()
        else:
            entries = self.db_model.filter(**filters)

        if ordering is not None:
            entries = entries.order_by(*ordering)

        if pagination is not None:
            entries = entries.limit(pagination["per_page"]).offset(
                pagination["per_page"] * pagination["page"]
            )

        return [self.domain_model.from_orm(entry) for entry in await entries]


class EventDBRepository(DBRepository[db_models.EventModel, models.EventModel]):
    """Event database repository."""

    db_model = db_models.EventModel
    domain_model = models.EventModel

    async def group_by(self, field: str, min_count: int | None = None) -> list[dict]:
        """Group events by given field."""
        query = (
            self.db_model.filter(**{f"{field}__isnull": False})
            .group_by(field)
            .annotate(count=functions.Count(field))
        )
        if min_count:
            query = query.filter(count__gte=min_count)
        return list(await query.order_by("-count").values(field, "count"))


class HookDBRepository(DBRepository[db_models.HookModel, models.HookModel]):
    """Hook database repository."""

    db_model = db_models.HookModel
    domain_model = models.HookModel

    async def update(self, uid: uuid.UUID, data: dict) -> models.HookModel:
        """Update hook with given data."""
        hook = await self.db_model.get_or_none(id=uid)
        if hook is None:
            raise exceptions.NotFoundError()
        hook.update_from_dict(data)
        await hook.save()
        return self.domain_model.from_orm(hook)

    async def delete(self, uid: uuid.UUID) -> None:
        """Delete hook."""
        hook = await self.db_model.get(id=uid)
        await hook.delete()
