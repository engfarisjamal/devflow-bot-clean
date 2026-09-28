"""Unit tests for use cases."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from devflow_bot.application.use_cases.handle_github_event import HandleGitHubEventUseCase
from devflow_bot.domain.entities.github_event import GitHubEvent
from devflow_bot.domain.entities.project import Project
from devflow_bot.domain.value_objects.event_type import EventType


@pytest.mark.asyncio
async def test_handle_github_event_push() -> None:
    """Test handling a push event."""
    event_repo = MagicMock()
    event_repo.add = AsyncMock()
    event_repo.update = AsyncMock()

    notification_repo = MagicMock()
    notification_repo.add = AsyncMock()

    project_repo = MagicMock()
    project_repo.get_by_repository = AsyncMock(
        return_value=Project(
            id="p1",
            name="Test",
            repository="user/repo",
            owner="user",
            chat_id="12345",
        )
    )
    project_repo.update = AsyncMock()

    use_case = HandleGitHubEventUseCase(event_repo, notification_repo, project_repo)

    payload = {
        "_event_name": "push",
        "id": "evt-1",
        "repository": {"full_name": "user/repo"},
        "sender": {"login": "testuser"},
        "ref": "refs/heads/main",
        "commits": [{"id": "1"}, {"id": "2"}],
    }

    result = await use_case.execute(payload)

    assert result.event_type == EventType.PUSH
    assert result.repository == "user/repo"
    assert event_repo.add.called
    assert notification_repo.add.called
