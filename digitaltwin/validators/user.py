from .base import BaseValidator
from digitaltwin.constants.users import USER_NAME_REGEXP, DESCRIPTION_KEY_REGEXP
from re import match


class UserValidator(BaseValidator):
    def name(self, value: str):
        return match(USER_NAME_REGEXP, value), "Name is invalid"

    def description(self, data: str):
        for key in data.keys():
            if not match(DESCRIPTION_KEY_REGEXP, key):
                return False, f'Key "{key}" is invalid'
