"""Domain exceptions."""


class DomainError(Exception):
    """Base domain exception."""


class ProjectNotFoundError(DomainError):
    """Raised when project not found."""


class InvalidWebhookSignatureError(DomainError):
    """Raised when webhook signature is invalid."""


class NotificationError(DomainError):
    """Raised when notification fails."""


class EventProcessingError(DomainError):
    """Raised when event processing fails."""
