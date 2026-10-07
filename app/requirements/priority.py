from enum import Enum


class RequirementPriority(str, Enum):
    REQUIRED = "required"
    PREFERRED = "preferred"
    UNKNOWN = "unknown"