"""Integration tests for EventRepository."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from devflow_bot.domain.entities.github_event import GitHubEvent
from devflow_bot.domain.value_objects.event_type import EventType
from devflow_bot.infrastructure.database.repositories.sql_event_repository import (
    SQLEventRepository,
)


@pytest.mark.asyncio
async def test_add_and_get_event(db_session: AsyncSession) -> None:
    """Test adding and retrieving an event."""
    repo = SQLEventRepository(db_session)
    event = GitHubEvent(
        id="evt-1",
        event_type=EventType.PUSH,
        repository="user/repo",
        sender="tester",
        payload={"ref": "refs/heads/main"},
    )

    added = await repo.add(event)
    assert added.id == "evt-1"
    assert added.event_type == EventType.PUSH

    fetched = await repo.get_by_id("evt-1")
    assert fetched is not None
    assert fetched.repository == "user/repo"


@pytest.mark.asyncio
async def test_list_by_repository(db_session: AsyncSession) -> None:
    """Test listing events by repository."""
    repo = SQLEventRepository(db_session)

    for i in range(5):
        await repo.add(
            GitHubEvent(
                id=f"evt-{i}",
                event_type=EventType.PUSH,
                repository="user/repo",
                sender="tester",
                payload={},
            )
        )

    events = await repo.list_by_repository("user/repo")
    assert len(events) == 5


@pytest.mark.asyncio
async def test_list_unprocessed(db_session: AsyncSession) -> None:
    """Test listing unprocessed events."""
    repo = SQLEventRepository(db_session)

    e1 = GitHubEvent(
        id="e1", event_type=EventType.PUSH, repository="u/r", sender="t", payload={}
    )
    e2 = GitHubEvent(
        id="e2", event_type=EventType.PUSH, repository="u/r", sender="t", payload={}
    )
    e2.mark_processed()

    await repo.add(e1)
    await repo.add(e2)

    unprocessed = await repo.list_unprocessed()
    assert len(unprocessed) == 1
    assert unprocessed[0].id == "e1"
