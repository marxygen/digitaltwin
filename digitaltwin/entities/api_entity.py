from typing import Type
from digitaltwin.validators.base import BaseValidator
from digitaltwin.request import APICall
from digitaltwin.utils import join_urls
from digitaltwin.exceptions import (
    InvalidEntityDeclarationException,
    MissingEntityAttributesException,
)
from digitaltwin.constants.config import BaseConfig


class APIEntityMeta(type):
    """APIEntityMeta is a metaclass providing necessary functionality for the APIEntity subclasses"""

    def __new__(cls, name, bases, attrs):
        class_ = super(APIEntityMeta, cls).__new__(cls, name, bases, attrs)
        if class_.PK is not None and class_.PK not in class_._get_class_attrs():
            raise AttributeError(
                f"Field that is declared to be a primary key of the entity must be defined on {class_.__name__}: {class_.PK}"
            )
        return class_


class APIEntity(metaclass=APIEntityMeta):
    """Any Entity that is to be managed by the API"""

    CLIENT: "digitaltwin.client.DigitalTwinClient"  # Client to use
    READ_ONLY = False  # Whether this entity is read only
    URL_PATH = None  # URL path to this entity
    VALIDATOR: Type[BaseValidator] = None  # Validator to use for this entity
    JSON_EXEMPT = list()  # List of fields to be excluded from JSON representation
    PARENT: "APIEntity" = None  # Parent entity
    REQUIRES_PARENT = False  # Whether this entity requires a parent entity
    CONFIG_CLASS: Type[
        BaseConfig
    ] = None  # A class to allow to be used for more convenient configuration
    PK: str = None  # Unique identifier for this entity. Must be a field defined in class body.

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
        if self.VALIDATOR is not None and name in self.to_json().keys():
            self.VALIDATOR.validate(name, value)
        return super(APIEntity, self).__setattr__(name, value)

    def perform_request(self, api_call: APICall):
        """High-level wrapper to unify request interface"""
        return self.CLIENT.request(api_call)

    def __init_subclass__(cls) -> None:
        cls.URL_PATH = getattr(cls, "URL_PATH", None) or cls.__name__.lower() + "s"

    def get_url(self, generic=False) -> str:
        """Get URL for this entity

        Args:
            generic (bool, optional): If must be a generic url (/users/ instead of /users/<uuid>/). Defaults to False.

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
            getattr(self, self.PK) if not generic else None,
        )

    @classmethod
    def _get_class_attrs(cls) -> list:
        """Get class attributes

        Returns:
            list: List of class attributes
        """
        return [
            name
            for name in [*cls.__annotations__.keys(), *cls.__dict__.keys()]
            if not name.isupper() and not name.startswith("_")
        ]

    def _get_entity_attrs(self) -> list:
        """Get attributes of the entity"""
        return {
            name: type(getattr(self, name))
            for name in self._get_class_attrs()
            if not callable(getattr(self, name))
        }

    def __init__(self, config: Type[BaseConfig] = None, **kwargs):
        """Instantiate the APIEntity"""
        if self.CONFIG_CLASS and isinstance(config, self.CONFIG_CLASS):
            kwargs = config.to_dict()

        missing = [
            key
            for key in self._get_class_attrs()
            if key not in kwargs and key not in self.__annotations__
        ]
        if missing:
            raise MissingEntityAttributesException(
                f'{self.__class__.__name__} also requires the following attributes: {", ".join(missing)}'
            )
        for key, value in kwargs.items():
            if key not in self._get_class_attrs():
                raise AttributeError(
                    f'{self.__class__.__name__} does not take "{key}" as an argument'
                )
            setattr(self, key, value)

    def create(self) -> "APIEntity":
        """Create a new instance"""
        self.perform_request(
            APICall(url=self.get_url(generic=True), method="POST", data=self.to_json())
        )
        return self

    def get(self):
        """Fetch information about this entity"""
        self.perform_request(APICall(url=self.get_url(), method="GET"))
