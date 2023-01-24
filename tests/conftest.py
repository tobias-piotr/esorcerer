import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from esorcerer.app import app
from esorcerer.settings import settings


@pytest.fixture()
def test_app() -> FastAPI:
    """Create a test app with overridden dependencies."""
    return app


@pytest_asyncio.fixture()
async def http_client(test_app: FastAPI):
    """Create a http client."""
    async with AsyncClient(
        app=test_app,
        base_url=f"http://test{settings.API_PREFIX}",
    ) as client:
        yield client
