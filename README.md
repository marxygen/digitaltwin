# digitaltwin

# Overview

This package is built to allow quick and convenient access to DigitalTwin API

# Logging

This client ships with standard `digitaltwin_client` logger. You can redefine logger name by editing `constants.misc.LOGGER_NAME` variable.

# Users

To create a user,

# Usage

A central element of the package is the `DigitalTwinClient` class (`digitaltwin.client.DigitalTwinClient`).
You can initialize it with your **User Secret**:

```Python
from digitaltwin.client import DigitalTwinClient

client = DigitalTwinClient(user_secret="your_64_characters_long_secret")
```

**Note**: a `ValueError` will be raised if the secret is not 64 characters long!<br>
Any API call that needs to be made by entities is passed to the client to perform the request. Each entity has a `CLIENT` attribute
that holds current client instance. That means that the same entities may be used by different clients.

### Using the client

**Note:** this way is **not** reentrant save

```Python
with client:
    <entity>.create()
    <entity>.delete()
```

When the context is active, all `APIEntity` subclasses have the `CLIENT` attribute set to the client.

### Generating a user secret

If you don't have a user secret, you can use `generate_secret` method to generate it.

## Validators

Some entities might have constraints imposed on them, such as a regex expression. To address this, there are **validators** - classes specifically designed to validate a particular entity. **A separate validator is written for each entity**.

## Start your work on the platform

1. Create a role

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

# Creating new entities

### Defining classes

To define a new entity, subclass `digitaltwin.entities.APIEntity` and define new fields as follows:

```Python
from .api_entity import APIEntity


class Role(APIEntity):
    uuid: str = None
    name: str
    account: str = None
    rules: dict = None
    statement: dict
    created_ts: float = None
    updated_ts: float = None

```

You can also provide defaults.<br>
**Note:** Fields without defaults are considered _required_, whereas fields with defaults are not required.
