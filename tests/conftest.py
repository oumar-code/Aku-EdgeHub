"""Pytest configuration and shared fixtures for Aku-EdgeHub tests."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.db.session_sqlite import engine
from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Async HTTP test client bound to the Aku-EdgeHub ASGI app."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(autouse=True)
async def _dispose_sqlalchemy_engine() -> None:
    """Ensure asyncpg pooled connections are not reused across pytest event loops."""
    yield
    await engine.dispose()
