"""Abstract base class for video generation providers.

The VideoGenerator interface defines the contract that all providers
(fal.ai, Replicate, mock, etc.) must implement. Business logic in
VideoService depends only on this interface, never on concrete providers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class GenerationRequest:
    """Parameters for submitting a video generation job."""
    prompt: str
    negative_prompt: str | None = None
    aspect_ratio: str = "16:9"
    duration: int = 5
    style: str = "cinematic"


@dataclass(frozen=True)
class GenerationJob:
    """Handle returned immediately after submitting a generation request."""
    provider_job_id: str
    status: str = "queued"  # Initial status from the provider


@dataclass(frozen=True)
class GenerationStatus:
    """Current status of a generation job as reported by the provider."""
    status: str  # queued | processing | completed | failed
    video_url: str | None = None
    thumbnail_url: str | None = None
    error_message: str | None = None


class VideoGenerator(ABC):
    """Abstract base class for video generation providers.

    Implementations must handle:
    - Submitting generation requests
    - Checking job status
    - Returning video URLs on completion
    """

    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationJob:
        """Submit a video generation request to the provider.

        Returns a GenerationJob with the provider's job ID.
        Raises ProviderError if submission fails.
        """
        ...

    @abstractmethod
    async def get_status(self, provider_job_id: str) -> GenerationStatus:
        """Check the current status of a generation job.

        Returns GenerationStatus reflecting the provider's current state.
        """
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable name of this provider (e.g., 'fal')."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Model identifier used by this provider."""
        ...
