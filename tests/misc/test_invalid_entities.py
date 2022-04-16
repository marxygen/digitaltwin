import pytest
from digitaltwin.entities import APIEntity
from digitaltwin.client import DigitalTwinClient


def test_invalid_pk():
    with pytest.raises(AttributeError):

        class InvalidAPIEntity(APIEntity):
            PK = "foo"


def test_valid_entity():
    class ValidAPIEntity(APIEntity):
        PK = "foo"
        foo: str


def test_no_user_uuid():
    with pytest.raises(AssertionError):
        client = DigitalTwinClient()
        client.fetch_user()
