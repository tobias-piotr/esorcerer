import uuid

import nest_asyncio
import pytest

from esorcerer.domain import models, services
from esorcerer.plugins.tasks import periodic
from tests.unit.utils import InMemoryCacheRepository, InMemoryEventRepository

pytestmark = pytest.mark.usefixtures("use_db")


class TestPeriodicTasks:
    """Test cases for periodic tasks."""

    async def test_health_check(self):
        """Test health check task."""
        result = periodic.health_check()
        assert result == {"detail": "Ok"}

    async def test_create_projections(self, mocker):
        """Test create expensive projections task."""
        service = services.EventService(
            events=InMemoryEventRepository(),
            cache=InMemoryCacheRepository(),
        )
        mocker.patch(
            "esorcerer.plugins.tasks.periodic.get_event_service",
            return_value=service,
        )
        nest_asyncio.apply()

        result = periodic.create_expensive_projections()
        assert result == 0

        event_payload_1 = models.EventCreateModel(type="t1", entity_id=uuid.uuid4())
        event_payload_2 = models.EventCreateModel(type="t2", entity_id=uuid.uuid4())
        event_payload_3 = models.EventCreateModel(type="t3")
        for _ in range(5):
            # Create series of events for 2 entities
            await service.create(event_payload_1)
            await service.create(event_payload_2)
            # Additionally, have some with no entity attached
            await service.create(event_payload_3)

        result = periodic.create_expensive_projections()
        assert result == 2
