from .api_entity import APIEntity
from .user import User


class UserSecret(APIEntity):
    fingerprint: str
    account: str
    user: str
    validity_ts: float
    created_ts: float
    updated_ts: float

    PARENT = User
    URL = "secrets"
    REQUIRES_PARENT = True
