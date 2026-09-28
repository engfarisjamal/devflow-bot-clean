"""DTO for GitHub event."""

from pydantic import BaseModel, Field

from devflow_bot.domain.value_objects.event_type import EventType


class GitHubEventDTO(BaseModel):
    """Data transfer object for GitHub events."""

    event_type: EventType
    repository: str = Field(..., min_length=1)
    sender: str = Field(..., min_length=1)
    payload: dict = Field(default_factory=dict)
    branch: str | None = None
    commit_count: int = 0
