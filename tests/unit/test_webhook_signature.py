"""Unit tests for webhook signature verification."""

import hashlib
import hmac

from devflow_bot.presentation.webhooks.github_webhook import verify_signature


def test_verify_signature_valid() -> None:
    """Test valid signature."""
    payload = b'{"test": "data"}'
    secret = "mysecret"
    expected = "sha256=" + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()

    assert verify_signature(payload, expected, secret) is True


def test_verify_signature_invalid() -> None:
    """Test invalid signature."""
    payload = b'{"test": "data"}'
    secret = "mysecret"

    assert verify_signature(payload, "sha256=wrong", secret) is False


def test_verify_signature_empty() -> None:
    """Test empty signature."""
    assert verify_signature(b"data", "", "secret") is False
