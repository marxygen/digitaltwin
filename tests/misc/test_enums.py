from digitaltwin.constants import RoleConfig, Effect, Action


def test_role_config():
    role_config = RoleConfig()
    role_config.effect = Effect.ALLOW
    role_config.actions = [Action.CREATE_USER]

    data = role_config.to_dict()
    assert isinstance(data, dict)
    assert data == {"statement": {"effect": "allow", "actions": ["create_user"]}}
