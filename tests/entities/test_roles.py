from digitaltwin.entities import Role
from digitaltwin.client import DigitalTwinClient


def test_role_creation():
    client = DigitalTwinClient()
    role = Role(statement={"effect": "allow", "actions": ["create_user"]})

    with client:
        # role.create()
        ...
