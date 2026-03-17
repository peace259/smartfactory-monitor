from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sensor import SensorReading
from app.schemas.sensor import SensorReadingCreate


class SensorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_reading(self, data: SensorReadingCreate) -> SensorReading:
        reading = SensorReading(**data.model_dump())
        self.db.add(reading)
        await self.db.flush()
        await self.db.refresh(reading)
        return reading

    async def create_batch(self, readings: list[SensorReadingCreate]) -> list[SensorReading]:
        db_objects = [SensorReading(**r.model_dump()) for r in readings]
        self.db.add_all(db_objects)
        await self.db.flush()
        return db_objects

    async def get_readings(
        self,
        sensor_id: str | None = None,
        sensor_type: str | None = None,
        since: datetime | None = None,
        limit: int = 100,
    ) -> list[SensorReading]:
        query = select(SensorReading).order_by(SensorReading.recorded_at.desc())

        if sensor_id:
            query = query.where(SensorReading.sensor_id == sensor_id)
        if sensor_type:
            query = query.where(SensorReading.sensor_type == sensor_type)
        if since:
            query = query.where(SensorReading.recorded_at >= since)

        query = query.limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_latest_per_sensor(self) -> list[SensorReading]:
        """Returns the most recent reading for each unique sensor_id."""
        subquery = (
            select(SensorReading.sensor_id, SensorReading.recorded_at.label("max_ts"))
            .group_by(SensorReading.sensor_id)
            .subquery()
        )
        query = select(SensorReading).join(
            subquery,
            (SensorReading.sensor_id == subquery.c.sensor_id)
            & (SensorReading.recorded_at == subquery.c.max_ts),
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
