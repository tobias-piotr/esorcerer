import datetime
import uuid

import pytest

from esorcerer.domain import exceptions, models, services

pytestmark = [pytest.mark.asyncio]


# It's like poetry, it rhymes
class InMemoryEventRepository:
    def __init__(self) -> None:
        self.events: list[models.EventModel] = []

    async def create(self, data):
        event = models.EventModel(
            id=uuid.uuid4(),
            created_at=datetime.datetime.now(),
            **data,
        )
        self.events.append(event)
        return event

    async def get(self, uid):
        return next(event for event in self.events if event.id == uid)

    async def collect(
        self,
        filters=None,
        ordering=None,
        pagination=None,
    ):
        return self.events


class InMemoryCacheRepository:
    def __init__(self) -> None:
        self.cache: dict[str, bytes] = {}

    def set(self, key, data):
        self.cache[key] = data

    def get(self, key):
        return self.cache.get(key)


class TestEventService:
    """Test cases for the EventService."""

    def get_service(self) -> services.EventService:
        """Return initialized service."""
        return services.EventService(
            events=InMemoryEventRepository(),
            cache=InMemoryCacheRepository(),
        )

    async def test_create(self):
        """Test create method."""
        service = self.get_service()
        data = models.EventCreateModel(type="random-event", payload={})
        event = await service.create(data)
        assert event.id is not None
        assert event.type == "random-event"

    async def test_get(self):
        """Test get method."""
        service = self.get_service()
        data = models.EventCreateModel(type="random-event", payload={})
        created_event = await service.create(data)
        event = await service.get(created_event.id)
        assert event == created_event

    async def test_collect(self):
        """Test collect method."""
        service = self.get_service()
        data = models.EventCreateModel(type="random-event", payload={})
        event_1 = await service.create(data)
        event_2 = await service.create(data)
        events = await service.collect()
        assert events == [event_1, event_2]

    async def test_project(self):
        """Test creating projection."""
        service = self.get_service()
        entity_id = uuid.uuid4()

        first_event = await service.create(
            models.EventCreateModel(
                type="e1",
                entity_id=entity_id,
                payload={"name": "Jon Jones"},
            )
        )
        await service.create(
            models.EventCreateModel(
                type="e2",
                entity_id=entity_id,
                payload={"is_champ": True},
            )
        )
        last_event = await service.create(
            models.EventCreateModel(
                type="e3",
                entity_id=entity_id,
                payload={"is_champ": False},
            )
        )

        projection = await service.project(entity_id)
        assert projection == models.ProjectionModel(
            started_at=first_event.created_at,
            last_update_at=last_event.created_at,
            entries=3,
            entity_id=entity_id,
            body={"name": "Jon Jones", "is_champ": False},
        )

    async def test_project_no_events(self):
        """Test creating projection when there are no events."""
        service = self.get_service()
        with pytest.raises(exceptions.NotFoundException):
            await service.project(uuid.uuid4())

    async def test_project_with_cache(self):
        """Test returning projection directly from cache."""
        service = self.get_service()
        eid = uuid.uuid4()
        cached_projection = models.ProjectionModel(
            started_at=datetime.datetime.now(),
            last_update_at=datetime.datetime.now(),
            entries=100,
            entity_id=eid,
            body={"cached": True},
        )
        service.cache.set(str(eid), cached_projection.json())

        projection = await service.project(eid)
        assert projection == cached_projection
