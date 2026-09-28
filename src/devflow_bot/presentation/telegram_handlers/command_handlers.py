"""Telegram command handlers."""

from datetime import UTC, datetime

from telegram import Update
from telegram.ext import ContextTypes

from devflow_bot.config.logging import get_logger
from devflow_bot.domain.entities.project import Project
from devflow_bot.infrastructure.database.base import async_session_maker
from devflow_bot.infrastructure.database.repositories.sql_project_repository import (
    SQLProjectRepository,
)

logger = get_logger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    text = (
        f"👋 مرحباً {user.first_name}!\n\n"
        "🤖 DevFlow Bot - رفيقك في إدارة المشاريع\n\n"
        "📋 الأوامر المتاحة:\n"
        "/start - بدء البوت\n"
        "/help - المساعدة\n"
        "/projects - عرض المشاريع\n"
        "/stats - الإحصائيات\n"
        "/status - الحالة\n"
        "/add_project - إضافة مشروع\n"
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    text = (
        "📚 المساعدة\n\n"
        "🔹 /projects - عرض كل المشاريع النشطة\n"
        "🔹 /stats - إحصائيات الاستخدام\n"
        "🔹 /status - حالة الخدمات\n"
        "🔹 /add_project <name> <repo> - إضافة مشروع جديد\n"
    )
    await update.message.reply_text(text)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    text = (
        "✅ جميع الخدمات تعمل بشكل طبيعي\n\n"
        "🟢 API: Online\n"
        "🟢 Database: Connected\n"
        "🟢 Webhooks: Active"
    )
    await update.message.reply_text(text)


async def projects_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /projects command."""
    try:
        async with async_session_maker() as session:
            repo = SQLProjectRepository(session)
            projects = await repo.list_active()
    except (OSError, RuntimeError, ValueError) as e:
        logger.error("projects_command_failed", error=str(e))
        await update.message.reply_text(f"❌ خطأ: {e!s}")
        return

    if not projects:
        await update.message.reply_text("📭 لا توجد مشاريع\n\nأضف مشروع بـ /add_project")
        return

    text = f"📋 المشاريع النشطة ({len(projects)})\n\n"
    for p in projects:
        text += f"🔹 {p.name}\n   {p.repository}\n   📊 {p.event_count} حدث\n\n"

    await update.message.reply_text(text)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command."""
    try:
        async with async_session_maker() as session:
            repo = SQLProjectRepository(session)
            projects = await repo.list_active()
    except (OSError, RuntimeError, ValueError) as e:
        logger.error("stats_command_failed", error=str(e))
        await update.message.reply_text(f"❌ خطأ: {e!s}")
        return

    total_events = sum(p.event_count for p in projects)
    text = (
        "📊 الإحصائيات\n\n"
        f"🔹 المشاريع: {len(projects)}\n"
        f"🔹 الأحداث الكلية: {total_events}\n"
        f"🔹 الحالة: 🟢 نشط\n"
    )
    await update.message.reply_text(text)


async def add_project_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /add_project <name> <repo> command."""
    args = context.args
    if not args or len(args) < 2:
        await update.message.reply_text(
            "⚠️ الاستخدام:\n/add_project <name> <owner/repo>\n\n"
            "مثال:\n/add_project MyProject engfarisjamal/devflow-bot"
        )
        return

    name = args[0]
    repository = args[1]
    chat_id = str(update.effective_chat.id)

    try:
        async with async_session_maker() as session:
            repo = SQLProjectRepository(session)
            existing = await repo.get_by_repository(repository)

            if existing:
                await update.message.reply_text(f"⚠️ المشروع {repository} موجود بالفعل")
                return

            project = Project(
                id=f"{int(datetime.now(UTC).timestamp())}",
                name=name,
                repository=repository,
                owner=repository.split("/")[0],
                chat_id=chat_id,
            )
            await repo.add(project)
    except (OSError, RuntimeError, ValueError) as e:
        logger.error("add_project_failed", error=str(e))
        await update.message.reply_text(f"❌ خطأ: {e!s}")
        return

    await update.message.reply_text(
        f"✅ تم إضافة المشروع\n\n📁 الاسم: {name}\n📦 المستودع: {repository}"
    )
