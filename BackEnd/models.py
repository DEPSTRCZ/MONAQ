from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship
from decimal import Decimal
from typing import Optional, List
from datetime import datetime, timezone


def get_utc_now():
    return datetime.now(timezone.utc)
class Sensors(SQLModel, table=True):
    sensor_id: int = Field(default=None, primary_key=True)
    times_posted: int = Field(default=0)
    last_update: datetime = Field(default_factory=get_utc_now, nullable=False)

    records: List["Records"] = Relationship(back_populates="sensor")

class Records(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensors.sensor_id",unique=False)
    co2: int = Field(default=None, nullable=True)
    temperature: Decimal = Field(default=None, max_digits=4,decimal_places=2,nullable=True)
    humidity: Decimal = Field(default=None, max_digits=4,decimal_places=2,nullable=True)
    updated_at: datetime = Field(default_factory=get_utc_now, nullable=False)
    loc_lat: Decimal = Field(default=None, max_digits=8,decimal_places=6,nullable=True)
    loc_long: Decimal = Field(default=None, max_digits=8,decimal_places=6,nullable=True)

    sensor: Sensors = Relationship(back_populates="records")
