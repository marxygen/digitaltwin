class BaseConfig:
    """Base class for a dictionary-like configuration."""

    def to_dict(self):
        """Transform class data to a dictionary"""
        fields = {
            field: type(getattr(self, field))
            for field in (
                *self.__annotations__,
                *[
                    item
                    for item in self.__dict__.keys()
                    if item.isupper()
                    and not item.startswith("_")
                    and not callable(getattr(self, item))
                ],
            )
        }
        data = {}
        for field, type_ in fields.items():
            field_value = getattr(self, field)
            if not isinstance(field_value, type_):
                raise TypeError(f"Field '{field}' is not of type '{type_.__name__}'")

            if not isinstance(field_value, self.__class__):
                data[field] = field_value
            else:
                data[field] = (
                    field_value.to_dict()
                    if not isinstance(field_value, list)
                    else [entry.to_dict() for entry in field_value]
                )
        return {self.NAME: data}
