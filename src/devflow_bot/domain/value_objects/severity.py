"""Notification severity value object."""

from enum import StrEnum


class Severity(StrEnum):
    """Notification severity levels."""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
