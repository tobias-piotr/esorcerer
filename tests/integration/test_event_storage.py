import uuid

import pytest

from esorcerer.domain import models
from esorcerer.plugins.database.repositories import EventDBRepository

pytestmark = pytest.mark.usefixtures("use_db")


class TestEventDBRepository:
    """Test cases for event database repository."""

    async def test_order_by(self):
        """Test order by method."""
        repo = EventDBRepository()

        payload_1 = models.EventCreateModel(type="e1", entity_id=uuid.uuid4())
        await repo.create(payload_1.dict())
        await repo.create(payload_1.dict())
        payload_2 = models.EventCreateModel(type="e2", entity_id=uuid.uuid4())
        await repo.create(payload_2.dict())
        payload_3 = models.EventCreateModel(type="e3")
        await repo.create(payload_3.dict())

        grouped = await repo.group_by("entity_id")
        assert grouped == [
            {"entity_id": payload_1.entity_id, "count": 2},
            {"entity_id": payload_2.entity_id, "count": 1},
        ]

    async def test_order_by_with_min(self):
        """Test order by method with min_count parameter."""
        repo = EventDBRepository()

        payload_1 = models.EventCreateModel(type="e1", entity_id=uuid.uuid4())
        await repo.create(payload_1.dict())
        await repo.create(payload_1.dict())
        payload_2 = models.EventCreateModel(type="e2", entity_id=uuid.uuid4())
        await repo.create(payload_2.dict())

        grouped = await repo.group_by("entity_id", 2)
        assert grouped == [{"entity_id": payload_1.entity_id, "count": 2}]
