"""Notification repository interface."""

from abc import ABC, abstractmethod

from devflow_bot.domain.entities.notification import Notification


class NotificationRepository(ABC):
    """Abstract repository for Notification entity."""

    @abstractmethod
    async def add(self, notification: Notification) -> Notification:
        """Add new notification."""
        ...

    @abstractmethod
    async def get_by_id(self, notification_id: str) -> Notification | None:
        """Get notification by ID."""
        ...

    @abstractmethod
    async def list_pending(self) -> list[Notification]:
        """List pending notifications."""
        ...

    @abstractmethod
    async def update(self, notification: Notification) -> Notification:
        """Update notification."""
        ...
