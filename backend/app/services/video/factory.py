"""Provider factory — selects the VideoGenerator implementation
based on the VIDEO_PROVIDER environment variable.

Supported providers:
  - "mock" → MockVideoGenerator (no API keys required)
  - "huggingface" → HuggingFaceVideoGenerator
"""

from app.core.config import Settings
from app.services.video.base import VideoGenerator
from app.services.video.mock_provider import MockVideoGenerator
from app.services.video.hf_provider import HuggingFaceVideoGenerator


def create_video_generator(settings: Settings) -> VideoGenerator:
    """Create and return the configured video generation provider."""
    match settings.VIDEO_PROVIDER:
        case "mock":
            return MockVideoGenerator()
        case "huggingface":
            return HuggingFaceVideoGenerator(settings)
        case _:
            raise ValueError(
                f"Unknown VIDEO_PROVIDER: '{settings.VIDEO_PROVIDER}'. "
                f"Supported values: 'mock', 'huggingface'"
            )
