from esorcerer.domain import services
from esorcerer.plugins.cache.repositories import RedisRepository
from esorcerer.plugins.database.repositories import EventDBRepository


def get_event_service() -> services.EventService:
    """Initialize event service."""
    return services.EventService(
        events=EventDBRepository(),
        cache=RedisRepository(),
    )
