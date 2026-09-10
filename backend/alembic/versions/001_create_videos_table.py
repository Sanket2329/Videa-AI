"""Create videos table

Revision ID: 001
Revises: None
Create Date: 2026-09-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "videos",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),

        # Prompt data
        sa.Column("original_prompt", sa.Text(), nullable=False),
        sa.Column("enhanced_prompt", sa.Text(), nullable=True),
        sa.Column("negative_prompt", sa.Text(), nullable=True),

        # Configuration
        sa.Column("style", sa.String(20), nullable=False, server_default="cinematic"),
        sa.Column("aspect_ratio", sa.String(10), nullable=False, server_default="16:9"),
        sa.Column("duration", sa.Integer(), nullable=False, server_default="5"),

        # Provider tracking
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("provider_job_id", sa.String(255), nullable=True),

        # State machine
        sa.Column("status", sa.String(20), nullable=False, server_default="queued"),

        # Results
        sa.Column("video_url", sa.Text(), nullable=True),
        sa.Column("thumbnail_url", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),

        # Timestamps
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),

        # Constraints
        sa.CheckConstraint(
            "status IN ('queued', 'processing', 'completed', 'failed', 'timeout', 'cancelled')",
            name="valid_status",
        ),
        sa.CheckConstraint(
            "aspect_ratio IN ('16:9', '9:16', '1:1')",
            name="valid_aspect_ratio",
        ),
        sa.CheckConstraint(
            "style IN ('cinematic', 'realistic', 'anime', '3d', 'product')",
            name="valid_style",
        ),
        sa.CheckConstraint(
            "duration IN (5, 10)",
            name="valid_duration",
        ),
    )

    # Indexes for common query patterns
    op.create_index("idx_videos_created_at", "videos", ["created_at"])
    op.create_index("idx_videos_status", "videos", ["status"])
    op.create_index("idx_videos_provider_job_id", "videos", ["provider_job_id"])


def downgrade() -> None:
    op.drop_index("idx_videos_provider_job_id", table_name="videos")
    op.drop_index("idx_videos_status", table_name="videos")
    op.drop_index("idx_videos_created_at", table_name="videos")
    op.drop_table("videos")
