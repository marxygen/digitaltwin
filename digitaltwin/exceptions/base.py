from typing import Type


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
        self.description = description

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
            if getattr(exception, "on_status_code") == status_code
        ]
        return match or cls
