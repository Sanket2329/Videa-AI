"""Health check endpoint.

Returns application status, version, and configured provider information.
Used by Docker health checks and monitoring.
"""

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.common import ApiResponse

router = APIRouter()


class HealthData(dict):
    """Health check response data."""
    pass


@router.get(
    "/health",
    summary="Health Check",
    description="Returns the application status and configuration info.",
    response_model=ApiResponse,
)
async def health_check(
    settings: Settings = Depends(get_settings),
) -> ApiResponse:
    return ApiResponse.ok({
        "status": "healthy",
        "version": settings.APP_VERSION,
        "provider": settings.VIDEO_PROVIDER,
        "model": settings.VIDEO_MODEL,
    })
