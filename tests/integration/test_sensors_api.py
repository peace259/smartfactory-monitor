import pytest
from httpx import AsyncClient

from app.config import settings

HEADERS = {"X-API-Key": settings.API_KEY}


@pytest.mark.asyncio
async def test_create_sensor_reading(client: AsyncClient):
    payload = {
        "sensor_id": "sensor-001",
        "sensor_type": "temperature",
        "value": 72.5,
        "unit": "°C",
        "location": "Line A",
    }
    response = await client.post("/api/v1/sensors/", json=payload, headers=HEADERS)
    assert response.status_code == 201
    data = response.json()
    assert data["sensor_id"] == "sensor-001"
    assert data["value"] == 72.5


@pytest.mark.asyncio
async def test_create_reading_unauthorized(client: AsyncClient):
    response = await client.post(
        "/api/v1/sensors/",
        json={"sensor_id": "x", "sensor_type": "pressure", "value": 1.0, "unit": "bar"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_readings_empty(client: AsyncClient):
    response = await client.get("/api/v1/sensors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_batch_ingest(client: AsyncClient):
    payload = {
        "readings": [
            {"sensor_id": f"s-{i}", "sensor_type": "vibration", "value": float(i), "unit": "mm/s"}
            for i in range(5)
        ]
    }
    response = await client.post("/api/v1/sensors/batch", json=payload, headers=HEADERS)
    assert response.status_code == 201
    assert len(response.json()) == 5
