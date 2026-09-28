"""Unit tests for domain exceptions."""

import pytest

from devflow_bot.domain.exceptions.domain_exceptions import (
    DomainError,
    EventProcessingError,
    InvalidWebhookSignatureError,
    NotificationError,
    ProjectNotFoundError,
)


def test_domain_error_hierarchy() -> None:
    assert issubclass(ProjectNotFoundError, DomainError)
    assert issubclass(InvalidWebhookSignatureError, DomainError)
    assert issubclass(NotificationError, DomainError)
    assert issubclass(EventProcessingError, DomainError)


def test_raise_domain_error() -> None:
    with pytest.raises(ProjectNotFoundError):
        raise ProjectNotFoundError("Project not found")
