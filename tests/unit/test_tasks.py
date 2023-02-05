import uuid

import nest_asyncio

from esorcerer.domain import models, services
from esorcerer.plugins.tasks import tasks
from tests.unit.utils import (
    InMemoryCacheRepository,
    InMemoryEventRepository,
    InMemoryHookRepository,
    MockedTaskRunner,
)


class TestTasks:
    """Test cases for tasks."""

    def get_event_service(self, mocker) -> services.EventService:
        service = services.EventService(
            events=InMemoryEventRepository(),
            cache=InMemoryCacheRepository(),
            tasks_runner=MockedTaskRunner,
        )
        mock_s = mocker.patch("esorcerer.plugins.tasks.tasks.get_event_service")
        mock_s.return_value.__aenter__.return_value = service
        return service

    def get_hook_service(self, mocker) -> services.HookService:
        service = services.HookService(hooks=InMemoryHookRepository())
        mock_s = mocker.patch("esorcerer.plugins.tasks.tasks.get_hook_service")
        mock_s.return_value.__aenter__.return_value = service
        return service

    async def test_health_check(self):
        """Test health check task."""
        result = tasks.health_check()
        assert result == {"detail": "Ok"}

    async def test_create_projections(self, mocker):
        """Test create expensive projections task."""
        service = self.get_event_service(mocker)
        nest_asyncio.apply()

        result = tasks.create_expensive_projections()
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

        result = tasks.create_expensive_projections()
        assert result == 2

    async def test_run_active_hooks(self, mocker):
        """Test run active hooks task."""
        event_service = self.get_event_service(mocker)
        hook_service = self.get_hook_service(mocker)
        event = await event_service.create(models.EventCreateModel(type="t1"))

        result = tasks.run_active_hooks(str(event.id))
        assert result == 0

        await hook_service.create(models.HookCreateModel(name="Test 1", is_active=True))

        result = tasks.run_active_hooks(str(event.id))
        assert result == 1

    async def test_run_active_hooks_without_event(self, mocker):
        """Test run active hooks task, when event was not found."""
        self.get_event_service(mocker)  # To mock the service

        hook_service = self.get_hook_service(mocker)
        await hook_service.create(models.HookCreateModel(name="Test 1", is_active=True))

        result = tasks.run_active_hooks(str(uuid.uuid4()))
        # 0 even tho hook is there
        assert result == 0
