from .config import BaseConfig
from typing import List


class Effect(BaseConfig):
    ALLOW = "allow"
    DENY = "deny"


class Action(BaseConfig):
    CREATE_USER = "create_user"


class RoleConfig(BaseConfig):
    NAME = "statement"
    effect: Effect
    actions: List[Action]
