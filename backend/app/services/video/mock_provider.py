"""Mock video generation provider for development and testing.

Simulates the async video generation lifecycle (queued → processing →
completed) with configurable delays. Uses a sample video URL so the
frontend can render a real video player without spending API credits.

Enable with: VIDEO_PROVIDER=mock
"""

import uuid
from datetime import datetime, timezone

from app.core.logging import get_logger
from app.services.video.base import (
    GenerationJob,
    GenerationRequest,
    GenerationStatus,
    VideoGenerator,
)

logger = get_logger(__name__)

# A short, publicly available sample video for testing
SAMPLE_VIDEO_URL = (
    "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"
)


class MockVideoGenerator(VideoGenerator):
    """Simulates video generation with time-based state transitions."""

    def __init__(self) -> None:
        self._jobs: dict[str, dict] = {}

    async def generate(self, request: GenerationRequest) -> GenerationJob:
        """Create a mock generation job."""
        job_id = f"mock-{uuid.uuid4().hex[:12]}"
        self._jobs[job_id] = {
            "created_at": datetime.now(timezone.utc),
            "queue_seconds": 2,
            "processing_seconds": 6,
            "request": request,
        }
        logger.info(
            "mock_generation_submitted",
            provider_job_id=job_id,
            prompt_length=len(request.prompt),
        )
        return GenerationJob(provider_job_id=job_id, status="queued")

    async def get_status(self, provider_job_id: str) -> GenerationStatus:
        """Return mock status based on elapsed time since creation."""
        job = self._jobs.get(provider_job_id)
        if job is None:
            return GenerationStatus(
                status="failed",
                error_message="Mock job not found (server may have restarted)",
            )

        elapsed = (datetime.now(timezone.utc) - job["created_at"]).total_seconds()

        if elapsed < job["queue_seconds"]:
            return GenerationStatus(status="queued")
        elif elapsed < job["queue_seconds"] + job["processing_seconds"]:
            return GenerationStatus(status="processing")
        else:
            return GenerationStatus(
                status="completed",
                video_url=SAMPLE_VIDEO_URL,
            )

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def model_name(self) -> str:
        return "mock-v1"
