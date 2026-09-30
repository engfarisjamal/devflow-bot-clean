"""SQLAlchemy implementation of ProjectRepository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from devflow_bot.domain.entities.project import Project
from devflow_bot.domain.repositories.project_repository import ProjectRepository
from devflow_bot.infrastructure.database.models.project_model import ProjectModel


class SQLProjectRepository(ProjectRepository):
    """SQLAlchemy implementation."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_entity(self, model: ProjectModel) -> Project:
        return Project(
            id=model.id,
            name=model.name,
            repository=model.repository,
            owner=model.owner,
            chat_id=model.chat_id,
            created_at=model.created_at,
            active=model.active,
            event_count=model.event_count,
        )

    def _to_model(self, entity: Project) -> ProjectModel:
        return ProjectModel(
            id=entity.id,
            name=entity.name,
            repository=entity.repository,
            owner=entity.owner,
            chat_id=entity.chat_id,
            created_at=entity.created_at,
            active=entity.active,
            event_count=entity.event_count,
        )

    async def add(self, project: Project) -> Project:
        model = self._to_model(project)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, project_id: str) -> Project | None:
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.id == project_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_repository(self, repository: str) -> Project | None:
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.repository == repository)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_active(self) -> list[Project]:
        result = await self.session.execute(select(ProjectModel).where(ProjectModel.active))
        return [self._to_entity(m) for m in result.scalars().all()]

    async def update(self, project: Project) -> Project:
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.id == project.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Project {project.id} not found")

        model.name = project.name
        model.repository = project.repository
        model.owner = project.owner
        model.chat_id = project.chat_id
        model.active = project.active
        model.event_count = project.event_count

        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete(self, project_id: str) -> None:
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.id == project_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
