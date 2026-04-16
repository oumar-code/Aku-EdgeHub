"""Tests for the devices router (/api/v1/devices/...)."""

from __future__ import annotations

import uuid

from httpx import AsyncClient


def _unique_id() -> str:
    return f"test-{uuid.uuid4().hex[:12]}"


async def test_register_device_new(client: AsyncClient) -> None:
    device_id = _unique_id()
    payload = {
        "device_id": device_id,
        "name": "Test Sensor",
        "firmware_version": "1.0.0",
    }
    response = await client.post("/api/v1/devices/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["device_id"] == device_id
    assert data["status"] == "pending"


async def test_register_device_idempotent(client: AsyncClient) -> None:
    device_id = _unique_id()
    payload = {
        "device_id": device_id,
        "name": "Idempotent Sensor",
        "firmware_version": "2.0.0",
    }
    # First registration
    await client.post("/api/v1/devices/register", json=payload)
    # Second registration — must be idempotent
    response = await client.post("/api/v1/devices/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["device_id"] == device_id
    assert "already registered" in data["message"]


async def test_get_device_not_found(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/devices/{_unique_id()}")
    assert response.status_code == 404


async def test_get_device_found(client: AsyncClient) -> None:
    device_id = _unique_id()
    payload = {
        "device_id": device_id,
        "name": "Lookup Device",
        "firmware_version": "3.0.0",
        "capabilities": ["sensor"],
        "metadata": {"location": "lab"},
    }
    await client.post("/api/v1/devices/register", json=payload)

    response = await client.get(f"/api/v1/devices/{device_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == device_id
    assert data["name"] == "Lookup Device"
    assert data["firmware_version"] == "3.0.0"
    assert data["capabilities"] == ["sensor"]
