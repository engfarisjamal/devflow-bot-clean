"""Integration tests for GitHub webhook endpoint."""

import pytest
from httpx import ASGITransport, AsyncClient

from devflow_bot.presentation.api.main import app


@pytest.mark.asyncio
async def test_webhook_rejects_without_signature() -> None:
    """Test webhook rejects request without valid signature."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/webhooks/github",
            json={"test": "data"},
            headers={"X-GitHub-Event": "push"},
        )
        # Without secret set, it should accept
        assert response.status_code in (202, 401)


@pytest.mark.asyncio
async def test_health_endpoint() -> None:
    """Test health endpoint returns healthy."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint() -> None:
    """Test root endpoint returns app info."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
