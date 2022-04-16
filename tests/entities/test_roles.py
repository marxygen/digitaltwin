from digitaltwin.entities import Role
from digitaltwin.client import DigitalTwinClient
from digitaltwin.constants import RoleConfig, Effect, Action


def test_role_creation():
    client = DigitalTwinClient(
        "EbDNqD6IThQoR0Kcre72fq3GW52rMAVQvoxTOWuEmSbdh8Cw83pgcxXcLVXbR4Ad"
    )
    role_config = RoleConfig()
    role_config.effect = Effect.ALLOW
    role_config.actions = [Action.CREATE_USER]
    role = Role(role_config)

    with client:
        role.create()
