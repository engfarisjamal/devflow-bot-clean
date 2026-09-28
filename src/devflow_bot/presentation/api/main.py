"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession

from devflow_bot.config.logging import get_logger, setup_logging
from devflow_bot.config.settings import get_settings
from devflow_bot.domain.exceptions.domain_exceptions import DomainError
from devflow_bot.infrastructure.database.base import Base, async_session_maker, engine
from devflow_bot.presentation.api.dependencies.container import Container
from devflow_bot.presentation.api.middleware.error_handler import domain_exception_handler
from devflow_bot.presentation.webhooks.github_webhook import router as webhook_router

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown."""
    setup_logging()
    logger.info("app_starting", env=settings.app_env)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()
    logger.info("app_stopped")


app = FastAPI(
    title="DevFlow Bot",
    description="Autonomous Developer Workflow Bot",
    version="0.1.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def attach_container(request: Request, call_next):
    """Attach DI container to request state."""
    async with async_session_maker() as session:
        request.state.container = Container(session)
        request.state.session = session
        return await call_next(request)


app.add_exception_handler(DomainError, domain_exception_handler)

app.include_router(webhook_router)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.app_name}


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "docs": "/docs",
    }
