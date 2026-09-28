"""Use case: Handle GitHub webhook event."""

from datetime import UTC, datetime

from devflow_bot.application.dto.notification_dto import NotificationDTO
from devflow_bot.domain.entities.github_event import GitHubEvent
from devflow_bot.domain.entities.notification import Notification
from devflow_bot.domain.repositories.event_repository import EventRepository
from devflow_bot.domain.repositories.notification_repository import NotificationRepository
from devflow_bot.domain.repositories.project_repository import ProjectRepository
from devflow_bot.domain.value_objects.event_type import EventType
from devflow_bot.domain.value_objects.severity import Severity


class HandleGitHubEventUseCase:
    """Handle incoming GitHub webhook events."""

    def __init__(
        self,
        event_repo: EventRepository,
        notification_repo: NotificationRepository,
        project_repo: ProjectRepository,
    ) -> None:
        self.event_repo = event_repo
        self.notification_repo = notification_repo
        self.project_repo = project_repo

    async def execute(self, event_data: dict) -> GitHubEvent:
        """Process a GitHub event and create notification if needed."""
        event_type = self._detect_event_type(event_data)

        event = GitHubEvent(
            id=event_data.get("id", str(datetime.now(UTC).timestamp())),
            event_type=event_type,
            repository=event_data.get("repository", {}).get("full_name", "unknown"),
            sender=event_data.get("sender", {}).get("login", "unknown"),
            payload=event_data,
        )

        await self.event_repo.add(event)

        project = await self.project_repo.get_by_repository(event.repository)
        if project:
            project.increment_event_count()
            await self.project_repo.update(project)

            notification_dto = self._build_notification(event, project.chat_id)
            if notification_dto:
                notification = Notification(
                    id=event.id,
                    title=notification_dto.title,
                    message=notification_dto.message,
                    severity=notification_dto.severity,
                    chat_id=notification_dto.chat_id,
                )
                await self.notification_repo.add(notification)

        event.mark_processed()
        await self.event_repo.update(event)

        return event

    def _detect_event_type(self, data: dict) -> EventType:
        """Detect event type from payload."""
        event_name = data.get("_event_name", "push")
        try:
            return EventType(event_name)
        except ValueError:
            return EventType.PUSH

    def _build_notification(self, event: GitHubEvent, chat_id: str) -> NotificationDTO | None:
        """Build notification for the event."""
        if event.event_type == EventType.PUSH:
            count = event.get_commit_count()
            return NotificationDTO(
                title=f"📦 Push to {event.repository}",
                message=f"{event.sender} pushed {count} commit(s) to {event.get_branch()}",
                severity=Severity.INFO,
                chat_id=chat_id,
            )
        elif event.event_type == EventType.PULL_REQUEST:
            action = event.payload.get("action", "opened")
            pr_number = event.payload.get("number", "?")
            return NotificationDTO(
                title=f"🔀 Pull Request #{pr_number}",
                message=f"PR {action} in {event.repository}",
                severity=Severity.INFO,
                chat_id=chat_id,
            )
        elif event.event_type == EventType.ISSUES:
            action = event.payload.get("action", "opened")
            issue_number = event.payload.get("issue", {}).get("number", "?")
            return NotificationDTO(
                title=f"🐛 Issue #{issue_number}",
                message=f"Issue {action} in {event.repository}",
                severity=Severity.WARNING,
                chat_id=chat_id,
            )
        return None
