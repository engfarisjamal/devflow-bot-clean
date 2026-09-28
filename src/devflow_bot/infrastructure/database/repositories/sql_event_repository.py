"""SQLAlchemy implementation of EventRepository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from devflow_bot.domain.entities.github_event import GitHubEvent
from devflow_bot.domain.repositories.event_repository import EventRepository
from devflow_bot.domain.value_objects.event_type import EventType
from devflow_bot.infrastructure.database.models.event_model import EventModel


class SQLEventRepository(EventRepository):
    """SQLAlchemy implementation."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_entity(self, model: EventModel) -> GitHubEvent:
        return GitHubEvent(
            id=model.id,
            event_type=EventType(model.event_type),
            repository=model.repository,
            sender=model.sender,
            payload=model.payload,
            created_at=model.created_at,
            processed=model.processed,
        )

    def _to_model(self, entity: GitHubEvent) -> EventModel:
        return EventModel(
            id=entity.id,
            event_type=entity.event_type.value,
            repository=entity.repository,
            sender=entity.sender,
            payload=entity.payload,
            created_at=entity.created_at,
            processed=entity.processed,
        )

    async def add(self, event: GitHubEvent) -> GitHubEvent:
        model = self._to_model(event)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, event_id: str) -> GitHubEvent | None:
        result = await self.session.execute(
            select(EventModel).where(EventModel.id == event_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_by_repository(
        self, repository: str, limit: int = 50
    ) -> list[GitHubEvent]:
        result = await self.session.execute(
            select(EventModel)
            .where(EventModel.repository == repository)
            .order_by(EventModel.created_at.desc())
            .limit(limit)
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def list_unprocessed(self) -> list[GitHubEvent]:
        result = await self.session.execute(
            select(EventModel).where(EventModel.processed == False)  # noqa: E712
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def update(self, event: GitHubEvent) -> GitHubEvent:
        result = await self.session.execute(
            select(EventModel).where(EventModel.id == event.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Event {event.id} not found")

        model.processed = event.processed
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)
