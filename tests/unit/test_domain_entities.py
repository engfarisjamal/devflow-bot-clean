"""Unit tests for domain entities."""

from datetime import datetime

import pytest

from devflow_bot.domain.entities.github_event import GitHubEvent
from devflow_bot.domain.entities.notification import Notification
from devflow_bot.domain.entities.project import Project
from devflow_bot.domain.value_objects.event_type import EventType
from devflow_bot.domain.value_objects.severity import Severity


class TestGitHubEvent:
    """Tests for GitHubEvent entity."""

    def test_create_event(self) -> None:
        event = GitHubEvent(
            id="evt-1",
            event_type=EventType.PUSH,
            repository="user/repo",
            sender="testuser",
            payload={},
        )
        assert event.id == "evt-1"
        assert event.event_type == EventType.PUSH
        assert event.processed is False

    def test_mark_processed(self) -> None:
        event = GitHubEvent(
            id="evt-1",
            event_type=EventType.PUSH,
            repository="user/repo",
            sender="testuser",
            payload={},
        )
        event.mark_processed()
        assert event.processed is True

    def test_get_commit_count_for_push(self) -> None:
        event = GitHubEvent(
            id="evt-1",
            event_type=EventType.PUSH,
            repository="user/repo",
            sender="testuser",
            payload={"commits": [{"id": "1"}, {"id": "2"}]},
        )
        assert event.get_commit_count() == 2

    def test_get_commit_count_for_non_push(self) -> None:
        event = GitHubEvent(
            id="evt-1",
            event_type=EventType.ISSUES,
            repository="user/repo",
            sender="testuser",
            payload={"commits": [{"id": "1"}]},
        )
        assert event.get_commit_count() == 0

    def test_get_branch(self) -> None:
        event = GitHubEvent(
            id="evt-1",
            event_type=EventType.PUSH,
            repository="user/repo",
            sender="testuser",
            payload={"ref": "refs/heads/main"},
        )
        assert event.get_branch() == "main"


class TestProject:
    """Tests for Project entity."""

    def test_create_project(self) -> None:
        project = Project(
            id="p1",
            name="Test Project",
            repository="user/repo",
            owner="user",
            chat_id="12345",
        )
        assert project.id == "p1"
        assert project.event_count == 0
        assert project.active is True

    def test_increment_event_count(self) -> None:
        project = Project(
            id="p1",
            name="Test",
            repository="user/repo",
            owner="user",
            chat_id="12345",
        )
        project.increment_event_count()
        project.increment_event_count()
        assert project.event_count == 2

    def test_deactivate(self) -> None:
        project = Project(
            id="p1",
            name="Test",
            repository="user/repo",
            owner="user",
            chat_id="12345",
        )
        project.deactivate()
        assert project.active is False


class TestNotification:
    """Tests for Notification entity."""

    def test_create_notification(self) -> None:
        notif = Notification(
            id="n1",
            title="Test",
            message="Message",
            severity=Severity.INFO,
            chat_id="12345",
        )
        assert notif.sent is False
        assert notif.sent_at is None

    def test_mark_sent(self) -> None:
        notif = Notification(
            id="n1",
            title="Test",
            message="Message",
            severity=Severity.INFO,
            chat_id="12345",
        )
        notif.mark_sent()
        assert notif.sent is True
        assert notif.sent_at is not None
        assert isinstance(notif.sent_at, datetime)
