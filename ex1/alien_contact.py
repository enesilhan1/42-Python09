import enum
import pydantic
import datetime

class ContactType(enum.Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"

class AlienContact(pydantic.BaseModel):
    contact_id: str = pydantic.Field(min_length=5, max_length=15)
    timestamp: datetime.datetime
    location: str = pydantic.Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = pydantic.Field(ge=0.0, le=10.0)
    duration_minutes: int = pydantic.Field(ge=1, le=1440)
    witness_count: int = pydantic.Field(ge=1, le=100)
    message_received: str | None = pydantic.Field(default=None, max_length=500)
    is_verified: bool = False

    @pydantic.model_validator(mode="after")
    def check_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contacts must be verified")
        if self.contact_type == ContactType.TELEPATHIC and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3 witnesses")
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals must have a message received")
        return self
