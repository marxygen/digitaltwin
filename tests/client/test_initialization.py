from digitaltwin.client import DigitalTwinClient
import pytest


def test_invalid_user_secret():
    with pytest.raises(ValueError):
        client = DigitalTwinClient(user_secret="haha")
