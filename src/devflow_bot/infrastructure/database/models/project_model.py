"""SQLAlchemy model for Project."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from devflow_bot.infrastructure.database.base import Base


class ProjectModel(Base):
    """Projects table."""

    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    repository: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    owner: Mapped[str] = mapped_column(String(100), nullable=False)
    chat_id: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    event_count: Mapped[int] = mapped_column(Integer, default=0)
