"""Pytest configuration and shared fixtures for Aku-EdgeHub tests."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    """Async HTTP test client bound to the Aku-EdgeHub ASGI app.

    Session-scoped so all tests share one event loop and one asyncpg connection
    pool, preventing "Future attached to a different loop" crashes that occur
    when asyncpg connections created in test N are reused in test N+1's loop.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
