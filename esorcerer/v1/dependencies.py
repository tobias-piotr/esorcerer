from esorcerer.domain import services
from esorcerer.plugins.cache.repositories import RedisRepository
from esorcerer.plugins.database.repositories import EventDBRepository, HookDBRepository
from esorcerer.plugins.tasks.runner import CeleryTaskRunner


def get_event_service() -> services.EventService:
    """Initialize event service."""
    return services.EventService(
        events=EventDBRepository(),
        cache=RedisRepository(),
        tasks_runner=CeleryTaskRunner,
    )


def get_hook_service() -> services.HookService:
    """Initialize hook service."""
    return services.HookService(hooks=HookDBRepository())
