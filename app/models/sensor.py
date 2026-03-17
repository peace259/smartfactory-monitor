from datetime import datetime, timezone

from sqlalchemy import Float, String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sensor_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    sensor_type: Mapped[str] = mapped_column(String(32), nullable=False)  # temperature | pressure | vibration
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(16), nullable=False)
    location: Mapped[str] = mapped_column(String(128), nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
