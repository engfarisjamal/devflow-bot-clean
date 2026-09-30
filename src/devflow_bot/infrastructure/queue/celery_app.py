"""Celery application configuration."""

from celery import Celery

from devflow_bot.config.settings import get_settings

settings = get_settings()

# Add SSL parameters for rediss:// URLs
redis_url = settings.redis_url
if redis_url.startswith("rediss://"):
    separator = "&" if "?" in redis_url else "?"
    redis_url = f"{redis_url}{separator}ssl_cert_reqs=CERT_NONE"

celery_app = Celery(
    "devflow_bot",
    broker=redis_url,
    backend=redis_url,
    include=["devflow_bot.infrastructure.queue.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,
    task_soft_time_limit=540,
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
    broker_use_ssl={"ssl_cert_reqs": "CERT_NONE"},
    redis_backend_use_ssl={"ssl_cert_reqs": "CERT_NONE"},
)
