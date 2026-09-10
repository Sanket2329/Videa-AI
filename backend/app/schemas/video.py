"""Pydantic schemas for video generation endpoints."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class VideoStatus(str, Enum):
    """Valid states in the generation state machine."""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class VideoStyle(str, Enum):
    """Supported style presets."""
    CINEMATIC = "cinematic"
    REALISTIC = "realistic"
    ANIME = "anime"
    THREE_D = "3d"
    PRODUCT = "product"


class AspectRatio(str, Enum):
    """Supported aspect ratios."""
    LANDSCAPE = "16:9"
    PORTRAIT = "9:16"
    SQUARE = "1:1"


class Duration(int, Enum):
    """Supported video durations in seconds."""
    SHORT = 5
    LONG = 10


class VideoGenerateRequest(BaseModel):
    """Request body for POST /api/v1/videos/generate."""
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The text prompt describing the desired video",
    )
    enhanced_prompt: str | None = Field(
        default=None,
        description="Optional pre-enhanced prompt (from the enhance endpoint)",
    )
    negative_prompt: str | None = Field(
        default=None,
        max_length=500,
        description="Things to avoid in the generated video",
    )
    style: VideoStyle = Field(
        default=VideoStyle.CINEMATIC,
        description="Visual style preset",
    )
    aspect_ratio: AspectRatio = Field(
        default=AspectRatio.LANDSCAPE,
        description="Video aspect ratio",
    )
    duration: Duration = Field(
        default=Duration.SHORT,
        description="Video duration in seconds",
    )


class VideoResponse(BaseModel):
    """Response schema for a video generation record."""
    id: uuid.UUID
    original_prompt: str
    enhanced_prompt: str | None = None
    negative_prompt: str | None = None
    style: str
    aspect_ratio: str
    duration: int
    provider: str
    model: str
    provider_job_id: str | None = None
    status: str
    video_url: str | None = None
    thumbnail_url: str | None = None
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class VideoDeleteResponse(BaseModel):
    """Response for DELETE /api/v1/videos/{id}."""
    deleted: bool = True
