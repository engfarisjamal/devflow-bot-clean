"""Notification entity."""

from dataclasses import dataclass, field
from datetime import datetime, timezone

from devflow_bot.domain.value_objects.severity import Severity


@dataclass
class Notification:
    """Represents a notification to be sent."""

    id: str
    title: str
    message: str
    severity: Severity
    chat_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    sent: bool = False
    sent_at: datetime | None = None

    def mark_sent(self) -> None:
        """Mark notification as sent."""
        self.sent = True
        self.sent_at = datetime.now(timezone.utc)
