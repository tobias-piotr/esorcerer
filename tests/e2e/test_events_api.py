import uuid

import pytest
from fastapi import encoders, status

from esorcerer.domain import models

pytestmark = pytest.mark.usefixtures("use_db")


class TestEventsAPI:
    """Test cases for events API."""

    base_url = "/api/v1/events"

    async def test_create(self, http_client):
        """Test create endpoint."""
        payload = models.EventCreateModel(type="something-happened-1")
        response = await http_client.post(self.base_url + "/", json=payload.dict())
        assert response.status_code == status.HTTP_201_CREATED
        assert models.EventModel(**response.json())

    async def test_get(self, http_client):
        """Test get endpoint."""
        payload = models.EventCreateModel(type="something-happened-2")
        response = await http_client.post(self.base_url + "/", json=payload.dict())
        assert response.status_code == status.HTTP_201_CREATED

        response = await http_client.get(self.base_url + f"/{response.json()['id']}")
        assert response.status_code == status.HTTP_200_OK

    async def test_collect(self, http_client):
        """Test list endpoint."""
        for _ in range(3):
            payload = models.EventCreateModel(type="something-happened-3")
            response = await http_client.post(self.base_url + "/", json=payload.dict())
            assert response.status_code == status.HTTP_201_CREATED

        response = await http_client.get(self.base_url + "/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3

    async def test_collect_with_pagination(self, http_client):
        """Test list endpoint with pagination parameters."""
        for _ in range(3):
            payload = models.EventCreateModel(type="something-happened-4")
            response = await http_client.post(self.base_url + "/", json=payload.dict())
            assert response.status_code == status.HTTP_201_CREATED

        response = await http_client.get(self.base_url + "/?page=0&per_page=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

        response = await http_client.get(self.base_url + "/?page=1&per_page=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    async def test_collect_with_filters(self, http_client):
        """Test list endpoint with filter parameters."""
        await http_client.post(
            self.base_url + "/",
            json=models.EventCreateModel(type="something-happened-5").dict(),
        )
        await http_client.post(
            self.base_url + "/",
            json=models.EventCreateModel(type="something-happened-6").dict(),
        )

        response = await http_client.get(self.base_url + "/?type=something-happened-5")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    async def test_collect_with_ordering(self, http_client):
        """Test list endpoint with ordering parameters."""
        first_event = await http_client.post(
            self.base_url + "/",
            json=models.EventCreateModel(type="something-happened-7").dict(),
        )
        await http_client.post(
            self.base_url + "/",
            json=models.EventCreateModel(type="something-happened-8").dict(),
        )

        response = await http_client.get(self.base_url + "/?order_by=-created_at")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2
        assert response.json()[-1]["id"] == first_event.json()["id"]

    async def test_project(self, http_client):
        """Test project endpoint."""
        entity_id = uuid.uuid4()

        first_event = await http_client.post(
            self.base_url + "/",
            json=encoders.jsonable_encoder(
                models.EventCreateModel(
                    type="e1", entity_id=entity_id, payload={"name": "Daniel Cormier"}
                ).dict()
            ),
        )
        await http_client.post(
            self.base_url + "/",
            json=encoders.jsonable_encoder(
                models.EventCreateModel(
                    type="e2", entity_id=entity_id, payload={"is_champ": False}
                ).dict()
            ),
        )
        last_event = await http_client.post(
            self.base_url + "/",
            json=encoders.jsonable_encoder(
                models.EventCreateModel(
                    type="e3", entity_id=entity_id, payload={"is_champ": True}
                ).dict()
            ),
        )

        projection_response = await http_client.get(
            self.base_url + f"/project/{entity_id}"
        )
        expected_projection = models.ProjectionModel(
            created_at=first_event.json()["created_at"],
            last_update_at=last_event.json()["created_at"],
            entries=3,
            entity_id=entity_id,
            body={"name": "Daniel Cormier", "is_champ": True},
        )
        assert projection_response.json() == encoders.jsonable_encoder(
            expected_projection.dict()
        )
