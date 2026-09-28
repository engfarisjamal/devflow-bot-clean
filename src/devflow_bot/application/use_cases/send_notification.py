"""Use case: Send pending notifications."""

from devflow_bot.domain.repositories.notification_repository import NotificationRepository


class SendNotificationUseCase:
    """Send pending notifications via Telegram."""

    def __init__(self, notification_repo: NotificationRepository, bot) -> None:
        self.notification_repo = notification_repo
        self.bot = bot

    async def execute(self) -> int:
        """Send all pending notifications. Returns count sent."""
        pending = await self.notification_repo.list_pending()
        sent_count = 0

        for notification in pending:
            try:
                emoji = self._get_emoji(notification.severity.value)
                text = f"{emoji} *{notification.title}*\n\n{notification.message}"
                await self.bot.send_message(
                    chat_id=notification.chat_id,
                    text=text,
                    parse_mode="Markdown",
                )
                notification.mark_sent()
                await self.notification_repo.update(notification)
                sent_count += 1
            except Exception:
                continue

        return sent_count

    def _get_emoji(self, severity: str) -> str:
        """Get emoji for severity."""
        return {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "critical": "🚨",
        }.get(severity, "ℹ️")
