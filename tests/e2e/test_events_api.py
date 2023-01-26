import pytest
from fastapi import status

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
