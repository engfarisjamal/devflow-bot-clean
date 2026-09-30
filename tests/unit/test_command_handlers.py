"""Unit tests for Telegram command handlers."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from devflow_bot.presentation.telegram_handlers.command_handlers import (
    add_project_command,
    help_command,
    projects_command,
    start_command,
    stats_command,
    status_command,
)


def make_update(text: str = "/start") -> MagicMock:
    """Create a fake Update object."""
    update = MagicMock()
    update.effective_user.first_name = "Faris"
    update.effective_chat.id = 123
    update.message.text = text
    update.message.reply_text = AsyncMock()
    return update


def make_context(args: list[str] | None = None) -> MagicMock:
    """Create a fake Context object."""
    ctx = MagicMock()
    ctx.args = args or []
    return ctx


@pytest.mark.asyncio
async def test_start_command() -> None:
    """Test /start command."""
    update = make_update("/start")
    await start_command(update, make_context())
    update.message.reply_text.assert_called_once()
    assert "DevFlow Bot" in update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_help_command() -> None:
    """Test /help command."""
    update = make_update("/help")
    await help_command(update, make_context())
    update.message.reply_text.assert_called_once()
    assert "المساعدة" in update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_status_command() -> None:
    """Test /status command."""
    update = make_update("/status")
    await status_command(update, make_context())
    update.message.reply_text.assert_called_once()
    assert "API" in update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_add_project_command_no_args() -> None:
    """Test /add_project without args."""
    update = make_update("/add_project")
    await add_project_command(update, make_context([]))
    update.message.reply_text.assert_called_once()
    assert "الاستخدام" in update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_add_project_command_one_arg() -> None:
    """Test /add_project with only one arg."""
    update = make_update("/add_project test")
    await add_project_command(update, make_context(["test"]))
    update.message.reply_text.assert_called_once()
    assert "الاستخدام" in update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_projects_command_empty() -> None:
    """Test /projects command with empty result."""
    update = make_update("/projects")

    with patch(
        "devflow_bot.presentation.telegram_handlers.command_handlers.SQLProjectRepository"
    ) as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.list_active = AsyncMock(return_value=[])
        mock_repo_class.return_value = mock_repo

        await projects_command(update, make_context())

        update.message.reply_text.assert_called_once()
        assert "لا توجد مشاريع" in update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_stats_command_empty() -> None:
    """Test /stats command with empty projects."""
    update = make_update("/stats")

    with patch(
        "devflow_bot.presentation.telegram_handlers.command_handlers.SQLProjectRepository"
    ) as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.list_active = AsyncMock(return_value=[])
        mock_repo_class.return_value = mock_repo

        await stats_command(update, make_context())

        update.message.reply_text.assert_called_once()
        assert "الإحصائيات" in update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_projects_command_with_data() -> None:
    """Test /projects command with data."""
    update = make_update("/projects")

    mock_project = MagicMock()
    mock_project.name = "Test"
    mock_project.repository = "user/repo"
    mock_project.event_count = 5

    with patch(
        "devflow_bot.presentation.telegram_handlers.command_handlers.SQLProjectRepository"
    ) as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.list_active = AsyncMock(return_value=[mock_project])
        mock_repo_class.return_value = mock_repo

        await projects_command(update, make_context())

        update.message.reply_text.assert_called_once()
        assert "Test" in update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_stats_command_with_data() -> None:
    """Test /stats command with data."""
    update = make_update("/stats")

    mock_project = MagicMock()
    mock_project.event_count = 10

    with patch(
        "devflow_bot.presentation.telegram_handlers.command_handlers.SQLProjectRepository"
    ) as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.list_active = AsyncMock(return_value=[mock_project])
        mock_repo_class.return_value = mock_repo

        await stats_command(update, make_context())

        update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_add_project_success() -> None:
    """Test /add_project success."""
    update = make_update("/add_project MyProject user/repo")

    with patch(
        "devflow_bot.presentation.telegram_handlers.command_handlers.SQLProjectRepository"
    ) as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.get_by_repository = AsyncMock(return_value=None)
        mock_repo.add = AsyncMock()
        mock_repo_class.return_value = mock_repo

        await add_project_command(update, make_context(["MyProject", "user/repo"]))

        update.message.reply_text.assert_called_once()
        assert "تم إضافة المشروع" in update.message.reply_text.call_args[0][0]


@pytest.mark.asyncio
async def test_add_project_existing() -> None:
    """Test /add_project with existing project."""
    update = make_update("/add_project MyProject user/repo")

    mock_existing = MagicMock()

    with patch(
        "devflow_bot.presentation.telegram_handlers.command_handlers.SQLProjectRepository"
    ) as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.get_by_repository = AsyncMock(return_value=mock_existing)
        mock_repo_class.return_value = mock_repo

        await add_project_command(update, make_context(["MyProject", "user/repo"]))

        update.message.reply_text.assert_called_once()
        assert "موجود بالفعل" in update.message.reply_text.call_args[0][0]
