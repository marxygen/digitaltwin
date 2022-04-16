# Exceptions

Exceptions are defined in `digitaltwin.exceptions` module. Base exception for `digitaltwin` is the `DigitalTwinException`.
There are different classes of exceptions defined for each submodule:

- API Exceptions<br>
  These exceptions are raised automatically when a request to DigitalTwin API does not succeed. They automatically receive **error_subcode**, description and trace from the request.<br>
  Subcode description will be provided automatically.
