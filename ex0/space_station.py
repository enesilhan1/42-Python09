import pydantic
import datetime

class SpaceStation(pydantic.BaseModel):
    station_id: str = pydantic.Field(min_length=3, max_length=10)
    name: str = pydantic.Field(min_length=1, max_length=50)
    crew_size: int = pydantic.Field(ge=1, le=20)
    power_level: float = pydantic.Field(ge=0.0, le=100.0)
    oxygen_level: float = pydantic.Field(ge=0.0, le=100.0)
    last_maintenance: datetime.datetime
    is_operational: bool = True
    notes: str | None = pydantic.Field(default=None, min_length=0, max_length=200)
