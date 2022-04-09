"""A module containing exceptions related to requests to the API"""

from .base import DigitalTwinException


class BadRequestException(DigitalTwinException):
    """The request was unacceptable, often due to missing a required parameter or malformed parameters."""

    on_status_code = 400
    ...


class AuthenticationRequiredException(DigitalTwinException):
    """Authentication failed or was not provided."""

    on_status_code = 401
    ...


class AccessForbiddenException(DigitalTwinException):
    """The User does not have permissions to perform the request."""

    on_status_code = 403
    ...


class NotFoundException(DigitalTwinException):
    """The requested resource does not exist."""

    on_status_code = 404
    ...


class InternalErrorException(DigitalTwinException):
    """The server encountered an internal error and was not able to complete the request."""

    on_status_code = 500
    ...
