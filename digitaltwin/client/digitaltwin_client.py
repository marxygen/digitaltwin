from digitaltwin.constants.users import USER_SECRET_LENGTH
from digitaltwin.request import APICall
import digitaltwin.entities.api_entity as api_entity


class DigitalTwinClient:
    """A client-side wrapper around DigitalTwin API"""

    user_secret: str

    @classmethod
    def setup(cls):
        ...

    def __init__(self, user_secret: str = None):
        if user_secret and len(str(user_secret)) != USER_SECRET_LENGTH:
            raise ValueError(
                f"User Secret must be a string {USER_SECRET_LENGTH} characters long"
            )
        self.user_secret = user_secret

    def request(self, api_call: APICall):
        """Perform a request and return the response"""
        return api_call.call(user_secret=self.user_secret)

    def __enter__(self):
        api_entity.APIEntity.CLIENT = self
        return self

    def __exit__(self, exc_type, exc_value, trace):
        api_entity.APIEntity.CLIENT = None
