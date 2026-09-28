"""Integration tests for ProjectRepository."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from devflow_bot.domain.entities.project import Project
from devflow_bot.infrastructure.database.repositories.sql_project_repository import (
    SQLProjectRepository,
)


@pytest.mark.asyncio
async def test_add_and_get_project(db_session: AsyncSession) -> None:
    """Test adding and retrieving a project."""
    repo = SQLProjectRepository(db_session)
    project = Project(
        id="test-1",
        name="Test Project",
        repository="user/test-repo",
        owner="user",
        chat_id="12345",
    )

    added = await repo.add(project)
    assert added.id == "test-1"
    assert added.name == "Test Project"

    fetched = await repo.get_by_id("test-1")
    assert fetched is not None
    assert fetched.repository == "user/test-repo"


@pytest.mark.asyncio
async def test_get_by_repository(db_session: AsyncSession) -> None:
    """Test getting project by repository name."""
    repo = SQLProjectRepository(db_session)
    project = Project(
        id="test-2",
        name="Test",
        repository="user/unique-repo",
        owner="user",
        chat_id="12345",
    )
    await repo.add(project)

    fetched = await repo.get_by_repository("user/unique-repo")
    assert fetched is not None
    assert fetched.id == "test-2"

    not_found = await repo.get_by_repository("user/nonexistent")
    assert not_found is None


@pytest.mark.asyncio
async def test_list_active_projects(db_session: AsyncSession) -> None:
    """Test listing active projects."""
    repo = SQLProjectRepository(db_session)

    p1 = Project(id="p1", name="A", repository="u/a", owner="u", chat_id="1")
    p2 = Project(id="p2", name="B", repository="u/b", owner="u", chat_id="1")
    p3 = Project(id="p3", name="C", repository="u/c", owner="u", chat_id="1")
    p3.deactivate()

    await repo.add(p1)
    await repo.add(p2)
    await repo.add(p3)

    active = await repo.list_active()
    assert len(active) == 2
    assert all(p.active for p in active)


@pytest.mark.asyncio
async def test_update_project(db_session: AsyncSession) -> None:
    """Test updating a project."""
    repo = SQLProjectRepository(db_session)
    project = Project(
        id="test-3",
        name="Old Name",
        repository="u/update-test",
        owner="u",
        chat_id="12345",
    )
    await repo.add(project)

    project.name = "New Name"
    project.increment_event_count()
    updated = await repo.update(project)

    assert updated.name == "New Name"
    assert updated.event_count == 1


@pytest.mark.asyncio
async def test_delete_project(db_session: AsyncSession) -> None:
    """Test deleting a project."""
    repo = SQLProjectRepository(db_session)
    project = Project(
        id="test-4",
        name="To Delete",
        repository="u/delete-test",
        owner="u",
        chat_id="12345",
    )
    await repo.add(project)

    await repo.delete("test-4")
    fetched = await repo.get_by_id("test-4")
    assert fetched is None
