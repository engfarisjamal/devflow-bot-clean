"""Domain exceptions."""


class DomainError(Exception):
    """Base domain exception."""

    pass


class ProjectNotFoundError(DomainError):
    """Raised when project not found."""

    pass


class InvalidWebhookSignatureError(DomainError):
    """Raised when webhook signature is invalid."""

    pass


class NotificationError(DomainError):
    """Raised when notification fails."""

    pass


class EventProcessingError(DomainError):
    """Raised when event processing fails."""

    pass
