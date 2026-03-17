from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


SensorType = Literal["temperature", "pressure", "vibration"]


class SensorReadingCreate(BaseModel):
    sensor_id: str = Field(..., min_length=1, max_length=64, examples=["sensor-001"])
    sensor_type: SensorType
    value: float = Field(..., description="Raw measured value")
    unit: str = Field(..., max_length=16, examples=["°C", "bar", "mm/s"])
    location: str | None = Field(None, max_length=128, examples=["Line A"])

    @field_validator("value")
    @classmethod
    def value_must_be_finite(cls, v: float) -> float:
        import math
        if not math.isfinite(v):
            raise ValueError("value must be a finite number")
        return v


class SensorReadingOut(BaseModel):
    id: int
    sensor_id: str
    sensor_type: SensorType
    value: float
    unit: str
    location: str | None
    recorded_at: datetime

    model_config = {"from_attributes": True}


class SensorReadingBatch(BaseModel):
    readings: list[SensorReadingCreate] = Field(..., min_length=1, max_length=500)