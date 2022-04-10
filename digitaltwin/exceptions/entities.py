from .base import DigitalTwinException


class InvalidEntityDeclarationException(DigitalTwinException):
    """When an APIEntity is declared incorrectly"""

    ...


class MissingEntityAttributesException(DigitalTwinException):
    """When some of the required parameters have not been provided for the entity"""

    ...
