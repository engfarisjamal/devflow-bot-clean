"""Dependency injection container."""

from sqlalchemy.ext.asyncio import AsyncSession

from devflow_bot.application.use_cases.handle_github_event import HandleGitHubEventUseCase
from devflow_bot.infrastructure.database.repositories.sql_event_repository import (
    SQLEventRepository,
)
from devflow_bot.infrastructure.database.repositories.sql_notification_repository import (
    SQLNotificationRepository,
)
from devflow_bot.infrastructure.database.repositories.sql_project_repository import (
    SQLProjectRepository,
)


class Container:
    """Simple DI container."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._event_repo = SQLEventRepository(session)
        self._notification_repo = SQLNotificationRepository(session)
        self._project_repo = SQLProjectRepository(session)

    @property
    def event_repo(self) -> SQLEventRepository:
        return self._event_repo

    @property
    def notification_repo(self) -> SQLNotificationRepository:
        return self._notification_repo

    @property
    def project_repo(self) -> SQLProjectRepository:
        return self._project_repo

    def handle_github_event_use_case(self) -> HandleGitHubEventUseCase:
        return HandleGitHubEventUseCase(
            event_repo=self._event_repo,
            notification_repo=self._notification_repo,
            project_repo=self._project_repo,
        )
