import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sensor import SensorReading
from app.config import settings

class AnomalyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_recent_readings(self, limit: int = 100):
        query = select(SensorReading).order_by(SensorReading.recorded_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    def to_dataframe(self, readings: list) -> pd.DataFrame:
        data = [
            {
                "sensor_id": r.sensor_id,
                "sensor_type": r.sensor_type,
                "value": r.value,
                "recorded_at": r.recorded_at,
            }
            for r in readings
        ]
        return pd.DataFrame(readings)