import digitaltwin.client
from typing import Type
from digitaltwin.validators.base import BaseValidator
from digitaltwin.request import APICall
from digitaltwin.utils import join_urls
from digitaltwin.exceptions import InvalidEntityDeclarationException


class APIEntityMeta(type):
    """APIEntityMeta is a metaclass providing necessary functionality for the APIEntity subclasses"""

    def __new__(cls, name, bases, attrs):
        class_ = super(APIEntityMeta, cls).__new__(cls, name, bases, attrs)
        # Set `URL_PATH` to equal plural lowercase class name (e.g. users, twins)
        class_.URL_PATH = name.lower() + "s"
        return class_


class APIEntity(metaclass=APIEntityMeta):
    """Any Entity that is to be managed by the API"""

    CLIENT: digitaltwin.client.DigitalTwinClient
    READ_ONLY = False
    URL_PATH = None
    VALIDATOR: Type[BaseValidator]
    JSON_EXEMPT = dict()
    PARENT: "APIEntity"
    REQUIRES_PARENT = False

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

    def __setattr__(self, name, value):
        """Handle attribute setting"""
        if self.VALIDATOR is not None and name not in self.to_json().keys():
            self.VALIDATOR.validate(name, value)
        return super(APIEntity, self).__setattr__(name, value)

    def perform_request(self, api_call: APICall):
        """High-level wrapper to unify request interface"""
        return self.CLIENT.request(api_call)

    def get_url(self, general=False) -> str:
        """Get URL for this entity

        Args:
            general (bool, optional): If must be a general url (/users/ instead of /users/someuser/). Defaults to True.

        Returns:
            str: a URL
        """
        if self.REQUIRES_PARENT and self.PARENT is None:
            raise InvalidEntityDeclarationException(
                f"Parent is required for {self.__class__.__name__} but is not set"
            )
        return join_urls(
            self.PARENT.get_url() if self.PARENT else None,
            self.URL_PATH,
            self.uuid if not general else None,
        )
