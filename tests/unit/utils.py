import datetime
import uuid
from collections import Counter

from esorcerer.domain import models


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

    async def group_by(self, field, min_count=None):
        values = [getattr(event, field) for event in self.events]
        return [
            {field: k, "count": v} for k, v in Counter(values).items() if k is not None
        ]


class InMemoryCacheRepository:
    def __init__(self) -> None:
        self.cache: dict[str, bytes] = {}

    def set(self, key, data):
        self.cache[key] = data

    def get(self, key):
        return self.cache.get(key)
