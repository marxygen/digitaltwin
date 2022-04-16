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
