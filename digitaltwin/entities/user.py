from digitaltwin.entities.api_entity import APIEntity
from digitaltwin.validators.user import UserValidator


class User(APIEntity):
    """DigitalTwin Platform User"""

    uuid: str
    name: str
    account: str
    role: str
    description: dict
    created_ts: float
    updated_ts: float

    VALIDATOR = UserValidator()
    PK = "uuid"
