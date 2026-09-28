"""DTO for Notification."""

from pydantic import BaseModel, Field

from devflow_bot.domain.value_objects.severity import Severity


class NotificationDTO(BaseModel):
    """Data transfer object for notifications."""

    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=4000)
    severity: Severity = Severity.INFO
    chat_id: str = Field(..., min_length=1)
