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

def main() -> None:
    try:
        contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.datetime(2024, 1, 15, 14, 30),
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )
    except pydantic.ValidationError as e:
        print(f"Unexpected error: {e.errors()[0]['msg']}")
        return

    print("Alien Contact Log Validation")
    print("======================================")
    
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    if contact.message_received is not None:
        print(f"Message: '{contact.message_received}'")

    print("\n======================================")

    try:
        invalid_contact = AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime.datetime(2024, 1, 16, 9, 15),
            location="Roswell, New Mexico",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=6.2,
            duration_minutes=30,
            witness_count=1,
        )
        print(f"Unexpected: {invalid_contact.contact_id} was accepted")
    except pydantic.ValidationError as e:
        print("Expected validation error:")
        message = e.errors()[0]["msg"]
        print(message.removeprefix("Value error, "))