"""Telegram bot client wrapper."""

from telegram import Bot
from telegram.error import TelegramError

from devflow_bot.config.logging import get_logger
from devflow_bot.config.settings import get_settings

logger = get_logger(__name__)


class TelegramBotClient:
    """Wrapper around Telegram Bot API."""

    def __init__(self) -> None:
        settings = get_settings()
        self.token = settings.telegram_bot_token
        self._bot: Bot | None = None

    @property
    def bot(self) -> Bot:
        """Get or create bot instance."""
        if self._bot is None:
            if not self.token:
                raise ValueError("TELEGRAM_BOT_TOKEN is not set")
            self._bot = Bot(token=self.token)
        return self._bot

    async def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
        """Send message to a chat."""
        try:
            await self.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
            logger.info("telegram_message_sent", chat_id=chat_id)
            return True
        except TelegramError as e:
            logger.error("telegram_send_failed", chat_id=chat_id, error=str(e))
            return False

    async def send_notification(
        self, chat_id: str, title: str, message: str, emoji: str = "ℹ️"
    ) -> bool:
        """Send formatted notification."""
        text = f"{emoji} *{title}*\n\n{message}"
        return await self.send_message(chat_id, text)
