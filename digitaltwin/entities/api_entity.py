import digitaltwin.client
from typing import Type
from digitaltwin.validators.base import BaseValidator


class APIEntityMeta(type):
    """APIEntityMeta is a metaclass providing necessary functionality for the APIEntity subclasses"""

    def __new__(cls, name, bases, attrs):
        klass = super(APIEntityMeta, cls).__new__(cls, name, bases, attrs)
        # Set `API_PREFIX` to equal lowercase class name
        klass.API_PREFIX = name.lower()
        return klass


class APIEntity(metaclass=APIEntityMeta):
    """Any Entity that is to be managed by the API"""

    CLIENT: digitaltwin.client.DigitalTwinClient
    READ_ONLY = False
    API_PREFIX = None
    VALIDATOR: Type[BaseValidator]
    JSON_EXEMPT = dict()

    def to_json(self):
        """Transform object to JSON representation"""
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
            and not callable(value)
            and not key.isupper()
            and key not in self.JSON_EXEMPT
        }

    @classmethod
    def from_json(cls, json: dict) -> "APIEntity":
        """Restore object from JSON representation

        Args:
            json (dict): JSON data

        Returns:
            APIEntity: APIEntity restored from JSON representation
        """
        entity = cls()
        for key, value in json.items():
            setattr(entity, key, value)
        return entity
