"""Integration tests for NotificationRepository."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from devflow_bot.domain.entities.notification import Notification
from devflow_bot.domain.value_objects.severity import Severity
from devflow_bot.infrastructure.database.repositories.sql_notification_repository import (
    SQLNotificationRepository,
)


@pytest.mark.asyncio
async def test_add_and_get_notification(db_session: AsyncSession) -> None:
    """Test adding and retrieving a notification."""
    repo = SQLNotificationRepository(db_session)
    notif = Notification(
        id="n1",
        title="Test",
        message="Hello",
        severity=Severity.INFO,
        chat_id="12345",
    )

    added = await repo.add(notif)
    assert added.id == "n1"

    fetched = await repo.get_by_id("n1")
    assert fetched is not None
    assert fetched.title == "Test"


@pytest.mark.asyncio
async def test_list_pending(db_session: AsyncSession) -> None:
    """Test listing pending notifications."""
    repo = SQLNotificationRepository(db_session)

    n1 = Notification(id="n1", title="T", message="M", severity=Severity.INFO, chat_id="1")
    n2 = Notification(id="n2", title="T", message="M", severity=Severity.INFO, chat_id="1")
    n2.mark_sent()

    await repo.add(n1)
    await repo.add(n2)

    pending = await repo.list_pending()
    assert len(pending) == 1
    assert pending[0].id == "n1"
