from fastapi import status


class TestInternalAPI:
    """Test cases for internal API."""

    async def test_health_check(self, http_client):
        """Check that health check returns healthy response."""
        response = await http_client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["detail"] == "Ok"
