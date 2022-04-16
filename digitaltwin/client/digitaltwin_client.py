from digitaltwin.constants.users import USER_SECRET_LENGTH
from digitaltwin.request import APICall
import digitaltwin.entities.api_entity as api_entity
from digitaltwin.entities import UserSecret
from digitaltwin.entities import User


class DigitalTwinClient:
    """A client-side wrapper around DigitalTwin API"""

    user_secret: str
    user_uuid: str
    user: User

    def __init__(
        self, user_secret: str = None, user_uuid: str = None, fetch_user: bool = False
    ):
        """Initialize DigitalTwin client
        def test_role_creation():

                    ValueError: If UserSecret is invalid
        """
        if user_secret and len(str(user_secret)) != USER_SECRET_LENGTH:
            raise ValueError(
                f"User Secret must be a string {USER_SECRET_LENGTH} characters long"
            )
        self.user_secret = user_secret
        self.user_uuid = user_uuid
        if fetch_user:
            self.fetch_user()

    def request(self, api_call: APICall):
        """Perform a request and return the response"""
        return api_call.call(user_secret=self.user_secret)

    def __enter__(self):
        api_entity.APIEntity.CLIENT = self
        return self

    def __exit__(self, exc_type, exc_value, trace):
        api_entity.APIEntity.CLIENT = None

    def fetch_user(self):
        """Fetch current user"""
        assert self.user_uuid is not None, "User UUID is required to fetch current user"
        self.user = User(uuid=self.user_uuid)
        self.user.CLIENT = self
        self.user.get()
        return self.user
