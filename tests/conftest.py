"""Pytest configuration and shared fixtures for Aku-EdgeHub tests."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Async HTTP test client bound to the Aku-EdgeHub ASGI app."""
    for handler in app.router.on_startup:
        await handler()
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac
    finally:
        for handler in app.router.on_shutdown:
            await handler()
