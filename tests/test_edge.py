"""Tests for the edge-hub domain router (/api/v1/...)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
from httpx import AsyncClient


async def test_offline_health_returns_200(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health/offline")
    assert response.status_code == 200


async def test_offline_health_response_body(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health/offline")
    data = response.json()
    assert data["status"] == "ok"
    assert "mode" in data
    assert "db_reachable" in data
    assert "timestamp" in data


async def test_cache_status_returns_200(client: AsyncClient) -> None:
    response = await client.get("/api/v1/cache/status")
    assert response.status_code == 200


async def test_cache_status_response_body(client: AsyncClient) -> None:
    response = await client.get("/api/v1/cache/status")
    data = response.json()
    assert "item_count" in data
    assert "disk_usage_bytes" in data
    assert "mode" in data


async def test_sync_trigger_accepted(client: AsyncClient) -> None:
    response = await client.post("/api/v1/sync/trigger", json={"force": False, "scope": []})
    assert response.status_code == 202
    data = response.json()
    assert "accepted" in data
    assert "message" in data


async def test_ai_infer_success(client: AsyncClient) -> None:
    """Covers relay_infer (sync.py) and the ai_infer happy path (edge.py)."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "text": "hello",
        "model": "gemma-3",
        "finish_reason": "stop",
        "usage": {"input_tokens": 3, "output_tokens": 5},
    }

    mock_http_client = AsyncMock()
    mock_http_client.__aenter__ = AsyncMock(return_value=mock_http_client)
    mock_http_client.__aexit__ = AsyncMock(return_value=False)
    mock_http_client.post = AsyncMock(return_value=mock_response)

    with patch("app.services.sync.httpx.AsyncClient", return_value=mock_http_client):
        response = await client.post("/api/v1/ai/infer", json={"prompt": "say hello"})

    assert response.status_code == 200
    body = response.json()
    assert body["text"] == "hello"


async def test_ai_infer_service_unavailable(client: AsyncClient) -> None:
    """Covers the RequestError exception path in ai_infer (edge.py)."""

    async def _relay_raise(payload: dict) -> dict:
        raise httpx.RequestError("service offline", request=httpx.Request("POST", "http://test/ai"))

    with patch("app.services.sync.relay_infer", _relay_raise):
        response = await client.post("/api/v1/ai/infer", json={"prompt": "test"})

    assert response.status_code == 503
