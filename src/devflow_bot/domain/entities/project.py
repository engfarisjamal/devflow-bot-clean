"""Project entity."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Project:
    """Represents a tracked project/repository."""

    id: str
    name: str
    repository: str
    owner: str
    chat_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    active: bool = True
    event_count: int = 0

    def increment_event_count(self) -> None:
        """Increment event counter."""
        self.event_count += 1

    def deactivate(self) -> None:
        """Deactivate project."""
        self.active = False
