from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_api_key
from app.schemas.sensor import SensorReadingBatch, SensorReadingCreate, SensorReadingOut
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post(
    "/",
    response_model=SensorReadingOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
async def create_sensor_reading(
    payload: SensorReadingCreate,
    db: AsyncSession = Depends(get_db),
):
    """Ingest a single sensor reading."""
    service = SensorService(db)
    return await service.create_reading(payload)


@router.post(
    "/batch",
    response_model=list[SensorReadingOut],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
async def create_sensor_readings_batch(
    payload: SensorReadingBatch,
    db: AsyncSession = Depends(get_db),
):
    """Ingest up to 500 sensor readings in one request."""
    service = SensorService(db)
    return await service.create_batch(payload.readings)


@router.get("/", response_model=list[SensorReadingOut])
async def list_sensor_readings(
    sensor_id: str | None = Query(None),
    sensor_type: str | None = Query(None),
    since: datetime | None = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """Query historical sensor readings with optional filters."""
    service = SensorService(db)
    return await service.get_readings(sensor_id, sensor_type, since, limit)


@router.get("/latest", response_model=list[SensorReadingOut])
async def get_latest_readings(db: AsyncSession = Depends(get_db)):
    """Get the most recent reading for every sensor."""
    service = SensorService(db)
    return await service.get_latest_per_sensor()
