"""Video storage abstraction.

Provides a clean interface for storing and retrieving video files.
For the internship demo, we use the provider's CDN URLs directly.
In production, this would be replaced with S3/GCS object storage.

Design decision: Provider-hosted URLs (fal CDN) are used directly
in this version because:
  1. fal.ai retains files for a configurable period
  2. Adding S3 would increase infrastructure complexity without
     demonstrating additional AI/ML engineering skill
  3. The abstraction is in place for future migration
"""

from abc import ABC, abstractmethod


class VideoStorage(ABC):
    """Abstract interface for video file storage."""

    @abstractmethod
    async def save(self, video_url: str, video_id: str) -> str:
        """Save a video and return a permanent URL.

        Args:
            video_url: The source URL to download from.
            video_id: Unique identifier for the video.

        Returns:
            A permanent URL where the video can be accessed.
        """
        ...

    @abstractmethod
    async def get_url(self, video_id: str) -> str | None:
        """Get the URL for a stored video.

        Returns None if the video does not exist.
        """
        ...


class ProviderHostedStorage(VideoStorage):
    """Pass-through storage that uses the provider's CDN URL directly.

    This is appropriate when the provider retains generated files
    for a sufficient period. For production, replace with S3Storage.
    """

    async def save(self, video_url: str, video_id: str) -> str:
        """Return the provider URL unchanged."""
        return video_url

    async def get_url(self, video_id: str) -> str | None:
        """Not applicable — URLs are stored in the database."""
        return None
