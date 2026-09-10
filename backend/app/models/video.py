"""SQLAlchemy model for the videos table.

Stores all generation metadata including prompts, configuration,
provider tracking, status, and results. Uses UUID primary keys
and CHECK constraints for data integrity.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class Video(Base):
    """Represents a video generation record."""

    __tablename__ = "videos"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Prompt data
    original_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    enhanced_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    negative_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Configuration
    style: Mapped[str] = mapped_column(
        String(20), nullable=False, default="cinematic"
    )
    aspect_ratio: Mapped[str] = mapped_column(
        String(10), nullable=False, default="16:9"
    )
    duration: Mapped[int] = mapped_column(Integer, nullable=False, default=5)

    # Provider tracking
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    provider_job_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    # State machine
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="queued"
    )

    # Results
    video_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('queued', 'processing', 'completed', 'failed', 'timeout', 'cancelled')",
            name="valid_status",
        ),
        CheckConstraint(
            "aspect_ratio IN ('16:9', '9:16', '1:1')",
            name="valid_aspect_ratio",
        ),
        CheckConstraint(
            "style IN ('cinematic', 'realistic', 'anime', '3d', 'product')",
            name="valid_style",
        ),
        CheckConstraint(
            "duration IN (5, 10)",
            name="valid_duration",
        ),
        Index("idx_videos_created_at", "created_at"),
        Index("idx_videos_status", "status"),
        Index("idx_videos_provider_job_id", "provider_job_id"),
    )

    def __repr__(self) -> str:
        return f"<Video id={self.id} status={self.status} style={self.style}>"
