"""Event repository interface."""

from abc import ABC, abstractmethod

from devflow_bot.domain.entities.github_event import GitHubEvent


class EventRepository(ABC):
    """Abstract repository for GitHubEvent entity."""

    @abstractmethod
    async def add(self, event: GitHubEvent) -> GitHubEvent:
        """Add new event."""
        ...

    @abstractmethod
    async def get_by_id(self, event_id: str) -> GitHubEvent | None:
        """Get event by ID."""
        ...

    @abstractmethod
    async def list_by_repository(self, repository: str, limit: int = 50) -> list[GitHubEvent]:
        """List events by repository."""
        ...

    @abstractmethod
    async def list_unprocessed(self) -> list[GitHubEvent]:
        """List unprocessed events."""
        ...

    @abstractmethod
    async def update(self, event: GitHubEvent) -> GitHubEvent:
        """Update event."""
        ...
