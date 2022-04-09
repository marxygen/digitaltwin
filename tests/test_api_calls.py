from digitaltwin.request import APICall
from digitaltwin.exceptions import AccessForbiddenException
import pytest


def test_access_forbidden():
    with pytest.raises(AccessForbiddenException):
        call = APICall(url="/test/me/")
