from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_mock import MockerFixture
from tortoise import Tortoise

from esorcerer.app import app
from esorcerer.settings import settings


@pytest.fixture()
def test_app() -> FastAPI:
    """Create a test app with overridden dependencies."""
    return app


@pytest_asyncio.fixture()
async def use_db() -> AsyncGenerator[None, None]:
    """Prepare a database for test usage."""
    await Tortoise.init(
        db_url="sqlite://:memory",
        modules={"models": ["esorcerer.plugins.database.models"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()


@pytest_asyncio.fixture()
async def http_client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create a http client."""
    async with AsyncClient(
        app=test_app,
        base_url=f"http://test{settings.API_PREFIX}",
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def mock_celery_runner(mocker: MockerFixture) -> None:
    """Mock the celery runner execution."""
    mocker.patch("esorcerer.plugins.tasks.runner.CeleryTaskRunner.run")
