from typing import Type
from digitaltwin.constants import api, misc
import logging

logger = logging.getLogger(misc.LOGGER_NAME)


class DigitalTwinException(Exception):
    """Base class for exceptions originating from DigitalTwin API"""

    def __init__(
        self,
        subcode: int = -1,
        trace: str = "No trace",
        description: str = "Digital Twin Exception",
        *args,
        **kwargs,
    ):
        self.subcode = subcode
        self.trace = trace
        self.description = description or api.ERROR_SUBCODES.get(subcode, "")
        logger.error(str(self))

    def __str__(self):
        return f"[{self.subcode}] {self.description} ({self.trace})"

    @classmethod
    def get_status_code_exception(cls, status_code) -> Type["DigitalTwinException"]:
        """Get Exception class based on request status code

        Args:
            status_code (int): Request status code (e.g. 500, 200, ...)

        Returns:
            Type[DigitalTwinException]: An exception class to be used
        """
        match = [
            exception
            for exception in cls.__subclasses__()
            if getattr(exception, "on_status_code", None) == status_code
        ]
        return match[0] if match else cls
