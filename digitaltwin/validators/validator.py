from typing import Union, Tuple


class BaseValidator:
    """A base class for Validators - a special class that provides field validation for APIEntities

    How validators are applied:
        1. An APIEntity must declare a validator in its VALIDATOR attribute
        2. When an attribute change is occurring, validator's method with name EQUAL TO the name of the attribute being changed is called.
        For example, to validate a field called 'name', define the following function:
        ```
        def name(self, value: str) -> Union[bool, Tuple[bool, str]]:
            '''Checks that the name is compliant with the regexp'''
            return re.match(r"[0-9A-Za-z][0-9A-Za-z_ \-]{0,30}[0-9A-Za-z]", value)
        ```
        This method must return a bool indicating if the attribute value is correct. You can also return
        a tuple, second member being the error message
    """

    def validate(self, field: str, value: str):
        """Validate a field

        Args:
            field (str): Name of the field
            value (str): Value of the field

        Raises:
            ValueError: If the value is invalid
        """
        field_valid = getattr(self, field)(value) if hasattr(self, field) else None
        error_message = f'Field "{field}" has an invalid value: "{value}"'
        if isinstance(field_valid, tuple):
            field_valid, error_message = field_valid

        if field_valid is None:
            return None

        if not field_valid:
            raise ValueError(error_message)
