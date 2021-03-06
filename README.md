# digitaltwin

# Overview

This package is built to allow quick and convenient access to DigitalTwin API

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
