import enum
import pydantic


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