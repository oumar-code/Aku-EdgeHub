"""Pytest configuration and shared fixtures for Aku-EdgeHub tests."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Pin every async test to the session-scoped event loop.

    pytest-asyncio 0.24 defaults async *test functions* to function scope even
    when fixtures are session-scoped.  The SQLAlchemy asyncpg engine is a
    module-level singleton whose connection pool binds connections to the event
    loop that first used them.  Running each test in a fresh, function-scoped
    loop causes "Future attached to a different loop" / "another operation is in
    progress" errors with asyncpg.  Forcing all async tests onto the shared
    session loop keeps the pool valid for the entire test run.
    """
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for item in items:
        if isinstance(item, pytest.Function) and item.get_closest_marker("asyncio"):
            item.add_marker(session_scope_marker, append=False)


@pytest.fixture
async def client() -> AsyncClient:
    """Async HTTP test client bound to the Aku-EdgeHub ASGI app."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
