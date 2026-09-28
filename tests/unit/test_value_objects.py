"""Unit tests for value objects."""

import pytest

from devflow_bot.domain.value_objects.event_type import EventType
from devflow_bot.domain.value_objects.severity import Severity


class TestEventType:
    """Tests for EventType enum."""

    def test_event_types_exist(self) -> None:
        assert EventType.PUSH == "push"
        assert EventType.PULL_REQUEST == "pull_request"
        assert EventType.ISSUES == "issues"
        assert EventType.RELEASE == "release"

    def test_event_type_from_string(self) -> None:
        assert EventType("push") == EventType.PUSH
        assert EventType("pull_request") == EventType.PULL_REQUEST

    def test_invalid_event_type(self) -> None:
        with pytest.raises(ValueError):
            EventType("invalid_event")


class TestSeverity:
    """Tests for Severity enum."""

    def test_severity_levels(self) -> None:
        assert Severity.INFO == "info"
        assert Severity.SUCCESS == "success"
        assert Severity.WARNING == "warning"
        assert Severity.ERROR == "error"
        assert Severity.CRITICAL == "critical"
