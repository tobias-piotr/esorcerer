import datetime
import uuid
from collections import Counter
from typing import Generic, TypeVar

from pydantic import BaseModel

from esorcerer.domain import exceptions, models

Model = TypeVar("Model", bound=BaseModel)

# It's like poetry, it rhymes
class InMemoryRepository(Generic[Model]):
    model: type[Model]

    def __init__(self) -> None:
        self.entries: list[Model] = []

    async def create(self, data):
        entry = self.model(
            id=uuid.uuid4(),
            created_at=datetime.datetime.now(),
            **data,
        )
        self.entries.append(entry)
        return entry

    async def get(self, uid):
        try:
            return next(
                (entry for entry in self.entries if entry.id == uid),  # type: ignore
            )
        except StopIteration:
            raise exceptions.NotFoundError from None

    async def collect(
        self,
        filters=None,
        ordering=None,
        pagination=None,
    ):
        return self.entries


class InMemoryEventRepository(InMemoryRepository[models.EventModel]):
    model = models.EventModel

    async def group_by(self, field, min_count=None):
        values = [getattr(event, field) for event in self.entries]
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


class MockedTaskRunner:
    @classmethod
    def run(cls, name, *args, **kwargs):
        pass


class InMemoryHookRepository(InMemoryRepository[models.HookModel]):
    model = models.HookModel

    async def update(self, uid, data):
        hook = await self.get(uid)
        i = self.entries.index(hook)
        new_hook = self.model(**hook.dict(), **data)
        self.entries[i] = new_hook
        return new_hook

    async def delete(self, uid):
        hook = await self.get(uid)
        i = self.entries.index(hook)
        self.entries.pop(i)
