"""GitHub webhook handler."""

import hashlib
import hmac

from fastapi import APIRouter, Header, HTTPException, Request, status

from devflow_bot.config.logging import get_logger
from devflow_bot.config.settings import get_settings
from devflow_bot.domain.exceptions.domain_exceptions import InvalidWebhookSignatureError
from devflow_bot.presentation.api.dependencies.container import Container

logger = get_logger(__name__)
router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify GitHub webhook signature."""
    if not signature or not secret:
        return False
    expected = "sha256=" + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/github", status_code=status.HTTP_202_ACCEPTED)
async def github_webhook(
    request: Request,
    x_github_event: str = Header(..., alias="X-GitHub-Event"),
    x_hub_signature_256: str = Header(default="", alias="X-Hub-Signature-256"),
) -> dict:
    """Receive and process GitHub webhook events."""
    settings = get_settings()
    body = await request.body()

    if settings.github_webhook_secret:
        if not verify_signature(body, x_hub_signature_256, settings.github_webhook_secret):
            raise InvalidWebhookSignatureError("Invalid webhook signature")

    payload = await request.json()
    payload["_event_name"] = x_github_event

    container: Container = request.state.container
    use_case = container.handle_github_event_use_case()

    event = await use_case.execute(payload)

    logger.info(
        "github_event_processed",
        event_id=event.id,
        event_type=event.event_type.value,
        repository=event.repository,
    )

    return {
        "status": "accepted",
        "event_id": event.id,
        "event_type": event.event_type.value,
    }
