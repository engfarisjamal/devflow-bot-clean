"""SQLAlchemy implementation of NotificationRepository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from devflow_bot.domain.entities.notification import Notification
from devflow_bot.domain.repositories.notification_repository import NotificationRepository
from devflow_bot.domain.value_objects.severity import Severity
from devflow_bot.infrastructure.database.models.notification_model import NotificationModel


class SQLNotificationRepository(NotificationRepository):
    """SQLAlchemy implementation."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_entity(self, model: NotificationModel) -> Notification:
        return Notification(
            id=model.id,
            title=model.title,
            message=model.message,
            severity=Severity(model.severity),
            chat_id=model.chat_id,
            created_at=model.created_at,
            sent=model.sent,
            sent_at=model.sent_at,
        )

    def _to_model(self, entity: Notification) -> NotificationModel:
        return NotificationModel(
            id=entity.id,
            title=entity.title,
            message=entity.message,
            severity=entity.severity.value,
            chat_id=entity.chat_id,
            created_at=entity.created_at,
            sent=entity.sent,
            sent_at=entity.sent_at,
        )

    async def add(self, notification: Notification) -> Notification:
        model = self._to_model(notification)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, notification_id: str) -> Notification | None:
        result = await self.session.execute(
            select(NotificationModel).where(NotificationModel.id == notification_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_pending(self) -> list[Notification]:
        result = await self.session.execute(
            select(NotificationModel).where(NotificationModel.sent == False)
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def update(self, notification: Notification) -> Notification:
        result = await self.session.execute(
            select(NotificationModel).where(NotificationModel.id == notification.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Notification {notification.id} not found")

        model.sent = notification.sent
        model.sent_at = notification.sent_at
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)
