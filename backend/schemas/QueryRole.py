"""types for apis"""
from enum import Enum


class QueryRoleType(str, Enum):
    """enum for query role"""
    system = "system"
    user = "user"
    assistant = "assistant"
    function = "function"
