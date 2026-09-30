"""Celery tasks."""

import asyncio
from datetime import datetime, timezone

from devflow_bot.config.logging import get_logger
from devflow_bot.infrastructure.queue.celery_app import celery_app

logger = get_logger(__name__)


@celery_app.task(name="devflow.send_notification", bind=True, max_retries=3)
def send_notification_task(self, notification_id: str) -> dict:
    """Send a notification asynchronously."""
    try:
        logger.info("notification_task_started", notification_id=notification_id)
        # In production, this would fetch from DB and send via Telegram
        return {
            "status": "success",
            "notification_id": notification_id,
            "sent_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        logger.error("notification_task_failed", error=str(exc))
        raise self.retry(exc=exc, countdown=60) from exc


@celery_app.task(name="devflow.process_event", bind=True, max_retries=5)
def process_event_task(self, event_id: str) -> dict:
    """Process a GitHub event asynchronously."""
    try:
        logger.info("event_task_started", event_id=event_id)
        return {
            "status": "success",
            "event_id": event_id,
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        logger.error("event_task_failed", error=str(exc))
        raise self.retry(exc=exc, countdown=30) from exc


@celery_app.task(name="devflow.health_check")
def health_check_task() -> dict:
    """Simple health check task."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}
