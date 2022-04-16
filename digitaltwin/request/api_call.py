import requests
from digitaltwin.constants import api, misc
from digitaltwin.exceptions.base import DigitalTwinException
from urllib.parse import urljoin
import logging

logger = logging.getLogger(misc.LOGGER_NAME)


class APICall:
    """
    Provides functionality to make requests to DigitalTwin API
    """

    url: str
    user_secret: str
    query_params: dict
    data: dict
    method: str
    kwargs: dict = dict()
    raise_exceptions: bool
    response: requests.Response

    def __init__(
        self,
        url: str,
        user_secret: str = None,
        query_params: dict = dict(),
        data: dict = dict(),
        method: str = "get",
        headers: dict = dict(),
        call=False,
        **kwargs,
    ):
        """Instantiate APICall and make a request (unless otherwise requested)

        Args:
            url (str): URL to make the request to. Domain will be added automatically
            user_secret (str, optional): User Secret. If not provided, MUST be provided when using `call()`
            query_params (dict, optional): Dictionary of query params. Defaults to dict().
            data (dict, optional): Request BODY. Defaults to dict().
            method (str, optional): Request method (`requests.<method>`). Defaults to "get".
            call (bool, optional): Whether a call must be made after instantiation. Defaults to True.
            headers (dict, optional): Dictionary of headers. Defaults to {}. Authorization credentials will be added automatically
        """
        self.url = urljoin(api.API_ROOT, url)
        self.user_secret = user_secret
        self.query_params = query_params
        self.data = data
        self.method = method.lower()
        self.kwargs = kwargs
        self.headers = headers

        if call:
            self.call()

    def call(self, user_secret: str = None) -> dict:
        """Make a call to DigitalTwin API

        Args:
            user_secret (str, optional): User Secret to sign the API call. Used if the value was not provided during APICall instantiation

        Raises:
            AttributeError: If `method` provided is not available
        """
        if not hasattr(requests, self.method):
            raise AttributeError(f"Unsupported method: '{self.method}'")

        self.response = getattr(requests, self.method)(
            url=self.url,
            params=self.query_params,
            data=self.data,
            **self.kwargs,
            headers={**self.headers, "Authorization": user_secret or self.user_secret},
        )
        logger.debug(
            f"{self.method.upper()}: {self.url}, STATUS: {self.response.status_code}"
        )
        # If a non successful response is returned, raise an appropriate exception
        if self.response.status_code % 100 != 2:
            raise DigitalTwinException.get_status_code_exception(
                status_code=self.response.status_code
            )(**self.response.json())

        return self.response.json()
