"""Project repository interface."""

from abc import ABC, abstractmethod

from devflow_bot.domain.entities.project import Project


class ProjectRepository(ABC):
    """Abstract repository for Project entity."""

    @abstractmethod
    async def add(self, project: Project) -> Project:
        """Add new project."""
        ...

    @abstractmethod
    async def get_by_id(self, project_id: str) -> Project | None:
        """Get project by ID."""
        ...

    @abstractmethod
    async def get_by_repository(self, repository: str) -> Project | None:
        """Get project by repository name."""
        ...

    @abstractmethod
    async def list_active(self) -> list[Project]:
        """List all active projects."""
        ...

    @abstractmethod
    async def update(self, project: Project) -> Project:
        """Update project."""
        ...

    @abstractmethod
    async def delete(self, project_id: str) -> None:
        """Delete project."""
        ...
