"""Global error handler middleware."""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from devflow_bot.domain.exceptions.domain_exceptions import (
    DomainError,
    InvalidWebhookSignatureError,
    ProjectNotFoundError,
)


async def domain_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle domain exceptions."""
    if isinstance(exc, ProjectNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": str(exc)},
        )
    if isinstance(exc, InvalidWebhookSignatureError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": str(exc)},
        )
    if isinstance(exc, DomainError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(exc)},
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error"},
    )
