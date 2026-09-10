"""VideoService — core business logic for video generation.

Orchestrates the generation lifecycle:
  1. Validate + create DB record
  2. Submit to provider
  3. Check status (lazily on poll)
  4. Handle timeouts and failures

State machine transitions are enforced here.
"""

import uuid
from datetime import datetime, timezone

from app.core.config import Settings
from app.core.exceptions import (
    DuplicateGenerationError,
    GenerationError,
    GenerationTimeoutError,
    NotFoundError,
)
from app.core.logging import get_logger
from app.models.video import Video
from app.repositories.video import VideoRepository
from app.services.video.base import GenerationRequest, VideoGenerator

logger = get_logger(__name__)

# Valid state transitions in the generation state machine
VALID_TRANSITIONS: dict[str, set[str]] = {
    "queued": {"processing", "completed", "failed", "cancelled"},
    "processing": {"completed", "failed", "timeout", "cancelled"},
}


class VideoService:
    """Business logic for video generation and status tracking."""

    def __init__(
        self,
        repository: VideoRepository,
        generator: VideoGenerator,
        settings: Settings,
    ) -> None:
        self._repo = repository
        self._generator = generator
        self._settings = settings

    async def create_generation(
        self,
        prompt: str,
        user_id: uuid.UUID,
        *,
        enhanced_prompt: str | None = None,
        negative_prompt: str | None = None,
        style: str = "cinematic",
        aspect_ratio: str = "16:9",
        duration: int = 5,
    ) -> Video:
        """Create a new video generation job.

        1. Check for duplicate active generations
        2. Create a database record
        3. Submit to the video provider
        4. Update the record with the provider's job ID
        """
        # Duplicate protection
        if await self._repo.has_active_generation():
            raise DuplicateGenerationError()

        # Create the database record
        video = Video(
            original_prompt=prompt,
            enhanced_prompt=enhanced_prompt,
            negative_prompt=negative_prompt,
            style=style,
            aspect_ratio=aspect_ratio,
            duration=duration,
            provider=self._generator.provider_name,
            model=self._generator.model_name,
            user_id=user_id,
            status="queued",
        )
        video = await self._repo.create(video)

        # Submit to the provider
        try:
            request = GenerationRequest(
                prompt=enhanced_prompt or prompt,
                negative_prompt=negative_prompt,
                aspect_ratio=aspect_ratio,
                duration=duration,
                style=style,
            )
            job = await self._generator.generate(request)

            # Update with provider job ID
            video = await self._repo.update_status(
                video.id,
                status="queued",
                provider_job_id=job.provider_job_id,
            )

            logger.info(
                "generation_submitted",
                generation_id=str(video.id),
                provider_job_id=job.provider_job_id,
                provider=self._generator.provider_name,
            )

        except Exception as exc:
            await self._repo.update_status(
                video.id,
                status="failed",
                error_message=str(exc),
            )
            logger.error(
                "generation_submission_failed",
                generation_id=str(video.id),
                error=str(exc),
            )
            raise GenerationError() from exc

        return video  # type: ignore[return-value]

    async def get_generation(self, video_id: uuid.UUID) -> Video:
        """Get a video record, refreshing status from the provider if needed."""
        video = await self._repo.get_by_id(video_id)
        if video is None:
            raise NotFoundError("Video generation")

        # If the generation is still active, check the provider for updates
        if video.status in ("queued", "processing") and video.provider_job_id:
            video = await self._check_and_update_status(video)

        return video

    async def get_history(self, limit: int = 5) -> list[Video]:
        """Return the most recent video generations."""
        return await self._repo.get_history(limit=limit)

    async def delete_generation(self, video_id: uuid.UUID) -> bool:
        """Delete a video generation record."""
        deleted = await self._repo.delete(video_id)
        if not deleted:
            raise NotFoundError("Video generation")
        return True

    async def _check_and_update_status(self, video: Video) -> Video:
        """Check the provider for status updates and apply valid transitions."""
        # Check for timeout
        elapsed = (datetime.now(timezone.utc) - video.created_at).total_seconds()
        if elapsed > self._settings.GENERATION_TIMEOUT_SECONDS:
            logger.warning(
                "generation_timeout",
                generation_id=str(video.id),
                elapsed_seconds=elapsed,
            )
            updated = await self._repo.update_status(
                video.id,
                status="timeout",
                error_message="Generation exceeded the maximum allowed time.",
            )
            return updated  # type: ignore[return-value]

        # Query the provider
        try:
            provider_status = await self._generator.get_status(video.provider_job_id)
        except Exception as exc:
            logger.error(
                "provider_status_check_failed",
                generation_id=str(video.id),
                error=str(exc),
            )
            # Don't fail the record on a transient status check error
            return video

        new_status = provider_status.status

        # Validate the state transition
        if new_status != video.status:
            allowed = VALID_TRANSITIONS.get(video.status, set())
            if new_status not in allowed:
                logger.warning(
                    "invalid_state_transition",
                    generation_id=str(video.id),
                    current_status=video.status,
                    attempted_status=new_status,
                )
                return video

            updated = await self._repo.update_status(
                video.id,
                status=new_status,
                video_url=provider_status.video_url,
                thumbnail_url=provider_status.thumbnail_url,
                error_message=provider_status.error_message,
            )

            logger.info(
                "generation_status_changed",
                generation_id=str(video.id),
                old_status=video.status,
                new_status=new_status,
            )
            return updated  # type: ignore[return-value]

        return video
