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

def main():
    try:
        station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2026-10-01T14:05:00",
        is_operational=True
    )
    except pydantic.ValidationError as e:
        print("=========================================")
        print(e)
        return
    