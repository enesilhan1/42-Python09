import enum
import pydantic

class ContactType(enum.Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"

class AlienContact(pydantic.BaseModel):
    pass

