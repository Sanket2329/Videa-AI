"""Repository layer for video database operations.

Encapsulates all direct database access for the videos table.
The service layer calls these methods — routes never access
the repository directly.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.video import Video

logger = get_logger(__name__)


class VideoRepository:
    """Data access layer for Video records."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, video: Video) -> Video:
        """Insert a new video record."""
        self._session.add(video)
        await self._session.flush()
        await self._session.refresh(video)
        logger.info("video_created", generation_id=str(video.id), status=video.status)
        return video

    async def get_by_id(self, video_id: uuid.UUID, user_id: uuid.UUID | None = None) -> Video | None:
        """Fetch a video by its primary key, optionally restricted to a user."""
        query = select(Video).where(Video.id == video_id)
        if user_id:
            query = query.where(Video.user_id == user_id)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def update_status(
        self,
        video_id: uuid.UUID,
        status: str,
        *,
        video_url: str | None = None,
        thumbnail_url: str | None = None,
        error_message: str | None = None,
        provider_job_id: str | None = None,
    ) -> Video | None:
        """Update the status and optional fields of a video record."""
        values: dict = {
            "status": status,
            "updated_at": datetime.now(timezone.utc),
        }
        if video_url is not None:
            values["video_url"] = video_url
        if thumbnail_url is not None:
            values["thumbnail_url"] = thumbnail_url
        if error_message is not None:
            values["error_message"] = error_message
        if provider_job_id is not None:
            values["provider_job_id"] = provider_job_id
        if status in ("completed", "failed", "timeout"):
            values["completed_at"] = datetime.now(timezone.utc)

        await self._session.execute(
            update(Video).where(Video.id == video_id).values(**values)
        )
        await self._session.flush()

        logger.info(
            "video_status_updated",
            generation_id=str(video_id),
            new_status=status,
        )
        return await self.get_by_id(video_id)

    async def get_history(self, user_id: uuid.UUID, limit: int = 5) -> list[Video]:
        """Return the most recent video generations for a user."""
        result = await self._session.execute(
            select(Video)
            .where(Video.user_id == user_id)
            .order_by(Video.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def delete(self, video_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """Delete a video record. Returns True if a record was deleted."""
        video = await self.get_by_id(video_id, user_id)
        if video is None:
            return False
        await self._session.delete(video)
        await self._session.flush()
        logger.info("video_deleted", generation_id=str(video_id))
        return True

    async def has_active_generation(self, user_id: uuid.UUID) -> bool:
        """Check if there's an active (queued/processing) generation for the user."""
        result = await self._session.execute(
            select(Video)
            .where(Video.user_id == user_id)
            .where(Video.status.in_(["queued", "processing"]))
            .limit(1)
        )
        return result.scalar_one_or_none() is not None
