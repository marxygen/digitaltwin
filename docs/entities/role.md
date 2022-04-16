# Create a role

```Python
from digitaltwin.entities import Role

user_role = Role(statement={"effect": "allow", "actions": ["create_user"]})
user_role.save()
```

If you want to omit defining role parameters as a dictionary, you can use a helper from `digitaltwin.constants`:

```Python
from digitaltwin.constants.roles import RoleConfig, Action, Effect

role_config = RoleConfig()
role_config.effect = Effect.ALLOW
role_config.actions = [Action.CREATE_USER]
```

and then pass the `role_config` object to the `Role` class as params. With this configuration you'll only need to pass in this object:

```Python
role = Role(role_config)
```
