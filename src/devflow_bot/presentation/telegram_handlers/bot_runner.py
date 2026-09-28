"""Telegram bot runner."""

from telegram.ext import Application, CommandHandler

from devflow_bot.config.logging import get_logger, setup_logging
from devflow_bot.config.settings import get_settings
from devflow_bot.presentation.telegram_handlers.command_handlers import (
    add_project_command,
    help_command,
    projects_command,
    start_command,
    stats_command,
    status_command,
)

logger = get_logger(__name__)


def create_application() -> Application:
    """Create Telegram application with handlers."""
    settings = get_settings()

    if not settings.telegram_bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set in .env")

    application = Application.builder().token(settings.telegram_bot_token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("projects", projects_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("add_project", add_project_command))

    return application


def run_bot() -> None:
    """Run the Telegram bot (blocking)."""
    setup_logging()
    logger.info("telegram_bot_starting")

    application = create_application()
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    run_bot()
