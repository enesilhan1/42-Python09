import enum
import pydantic
import datetime


class Rank(enum.Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"

class CrewMember(pydantic.BaseModel):
    member_id: str = pydantic.Field(min_length=3, max_length=10)
    name: str = pydantic.Field(min_length=2, max_length=50)
    rank: Rank
    age: int = pydantic.Field(ge=18, le=80)
    specialization: str = pydantic.Field(min_length=3, max_length=30)
    years_experience: int = pydantic.Field(ge=0, le=50)
    is_active: bool = True

class SpaceMission(pydantic.BaseModel):
    mission_id: str = pydantic.Field(min_length=5, max_length=15)
    mission_name: str = pydantic.Field(min_length=3, max_length=100)
    destination: str = pydantic.Field(min_length=3, max_length=50)
    launch_date: datetime.datetime
    duration_days: int = pydantic.Field(ge=1, le=3650)
    crew: list[CrewMember] = pydantic.Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = pydantic.Field(ge=1.0, le=10000.0)

    @pydantic.model_validator(mode="after")
    def check_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("mission_id must start with 'M'")
        has_leader = False
        for member in self.crew:
            if member.rank in (Rank.CAPTAIN, Rank.COMMANDER):
                has_leader = True
                break
        if not has_leader:
            raise ValueError("Mission must have at least one Commander or Captain")
        if self.duration_days > 365:
            experienced = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    experienced += 1
            if experienced * 2 < len(self.crew):
                raise ValueError(
                        "Long missions (> 365 days) need at least 50% "
                        "experienced crew (5+ years)"
                        )
        for member in self.crew: 
            if not member.is_active:
                raise ValueError("All crew members must be active")
        return self