from esorcerer.domain import services
from esorcerer.plugins.database import repositories


def get_event_service() -> services.EventService:
    """Initialize event service."""
    repository = repositories.EventDBRepository()
    return services.EventService(repository=repository)
