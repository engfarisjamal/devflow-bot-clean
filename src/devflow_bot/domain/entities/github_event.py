"""GitHub event entity."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from devflow_bot.domain.value_objects.event_type import EventType


@dataclass
class GitHubEvent:
    """Represents a GitHub webhook event."""

    id: str
    event_type: EventType
    repository: str
    sender: str
    payload: dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)
    processed: bool = False

    def mark_processed(self) -> None:
        """Mark event as processed."""
        self.processed = True

    def get_commit_count(self) -> int:
        """Get number of commits in push event."""
        if self.event_type != EventType.PUSH:
            return 0
        return len(self.payload.get("commits", []))

    def get_branch(self) -> str:
        """Get branch name."""
        ref = self.payload.get("ref", "")
        return ref.replace("refs/heads/", "") if ref else ""
