"""Pytest configuration and shared fixtures for Aku-EdgeHub tests."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    """Async HTTP test client bound to the Aku-EdgeHub ASGI app.

    Session-scoped so the SQLAlchemy engine (module-level singleton) and the
    app lifespan are only initialised once per test run, avoiding event-loop
    conflicts across tests.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
