from .api_entity import APIEntity
from digitaltwin.constants import RoleConfig


class Role(APIEntity):
    uuid: str = None
    name: str
    account: str = None
    rules: dict = None
    statement: dict
    created_ts: float = None
    updated_ts: float = None

    CONFIG_CLASS = RoleConfig
