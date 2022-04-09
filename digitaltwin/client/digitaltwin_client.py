from digitaltwin.constants.users import USER_SECRET_LENGTH
from digitaltwin.request import APICall


class DigitalTwinClient:
    """A client-side wrapper around DigitalTwin API"""

    user_secret: str

    @classmethod
    def setup(cls):
        ...

    def __init__(self, user_secret: str):
        if len(str(user_secret)) != USER_SECRET_LENGTH:
            raise ValueError(
                f"User Secret must be a string {USER_SECRET_LENGTH} characters long"
            )
        self.user_secret = user_secret

    def request(self, api_call: APICall):
        """Perform a request and return the response"""
        return api_call.call(user_secret=self.user_secret)
