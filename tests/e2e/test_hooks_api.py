import uuid

import pytest
from fastapi import status

from esorcerer.domain import models

pytestmark = pytest.mark.usefixtures("use_db")


class TestHooksAPI:
    """Test cases for hooks API."""

    base_url = "/api/v1/hooks"

    async def test_create(self, http_client):
        """Test create endpoint."""
        payload = models.HookCreateModel(name="Test", is_active=True)
        response = await http_client.post(self.base_url + "/", json=payload.dict())
        assert response.status_code == status.HTTP_201_CREATED
        assert models.HookModel(**response.json())

    async def test_get(self, http_client):
        """Test get endpoint."""
        payload = models.HookCreateModel(name="Test", is_active=True)
        response = await http_client.post(self.base_url + "/", json=payload.dict())
        assert response.status_code == status.HTTP_201_CREATED

        response = await http_client.get(self.base_url + f"/{response.json()['id']}")
        assert response.status_code == status.HTTP_200_OK

    async def test_collect(self, http_client):
        """Test list endpoint."""
        for _ in range(3):
            payload = models.HookCreateModel(name="Test", is_active=True)
            response = await http_client.post(self.base_url + "/", json=payload.dict())
            assert response.status_code == status.HTTP_201_CREATED

        response = await http_client.get(self.base_url + "/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3

    async def test_update(self, http_client):
        """Test patch endpoint."""
        response = await http_client.post(
            self.base_url + "/",
            json=models.HookCreateModel(name="Test", is_active=True).dict(),
        )
        assert response.status_code == status.HTTP_201_CREATED

        response = await http_client.patch(
            self.base_url + f"/{response.json()['id']}",
            json=models.HookUpdateModel(name="Test 2").dict(),
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Test 2"
        assert response.json()["is_active"] is True

    async def test_update_not_found(self, http_client):
        """Test patch endpoint, when there is no hook."""
        response = await http_client.patch(
            self.base_url + f"/{uuid.uuid4()}",
            json=models.HookUpdateModel(name="Test 2").dict(),
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete(self, http_client):
        """Test delete endpoint."""
        response = await http_client.post(
            self.base_url + "/",
            json=models.HookCreateModel(name="Test", is_active=True).dict(),
        )
        assert response.status_code == status.HTTP_201_CREATED

        response = await http_client.delete(self.base_url + f"/{response.json()['id']}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
