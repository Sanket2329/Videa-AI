"""Hugging Face video generation provider.

Uses the huggingface_hub AsyncInferenceClient to generate videos in the background.
Since HF text_to_video blocks until completion and returns raw bytes, we run it
in an asyncio background task and save the MP4 locally.
"""

import asyncio
import os
import uuid
from datetime import datetime, timezone

from huggingface_hub import AsyncInferenceClient

from app.core.config import Settings
from app.core.exceptions import ProviderError
from app.core.logging import get_logger
from app.services.video.base import (
    GenerationJob,
    GenerationRequest,
    GenerationStatus,
    VideoGenerator,
)

logger = get_logger(__name__)

class HuggingFaceVideoGenerator(VideoGenerator):
    """Hugging Face provider implementation using text-to-video."""

    def __init__(self, settings: Settings) -> None:
        if not settings.HF_TOKEN:
            raise ValueError("HF_TOKEN must be set when VIDEO_PROVIDER='huggingface'")
        
        self.client = AsyncInferenceClient(
            provider="fal-ai",
            api_key=settings.HF_TOKEN
        )
        self.model = "Wan-AI/Wan2.2-TI2V-5B"
        
        # In-memory store for background job state
        self._jobs: dict[str, dict] = {}
        
        # Ensure the static videos directory exists
        self.videos_dir = "static/videos"
        os.makedirs(self.videos_dir, exist_ok=True)

    async def _generate_task(self, job_id: str, prompt: str) -> None:
        """Background task that calls HF API and saves the video."""
        try:
            logger.info("hf_generation_started", job_id=job_id, prompt_length=len(prompt))
            self._jobs[job_id]["status"] = "processing"
            
            # This blocks asynchronously until the video is returned
            video_bytes = await self.client.text_to_video(
                prompt,
                model=self.model
            )
            
            filename = f"{job_id}.mp4"
            filepath = os.path.join(self.videos_dir, filename)
            
            with open(filepath, "wb") as f:
                f.write(video_bytes)
                
            # Update state with the URL path that FastAPI serves
            self._jobs[job_id]["status"] = "completed"
            base_url = os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000")
            self._jobs[job_id]["video_url"] = f"{base_url}/static/videos/{filename}"
            logger.info("hf_generation_completed", job_id=job_id, filepath=filepath)
            
        except Exception as e:
            logger.error("hf_generation_failed", job_id=job_id, error=str(e))
            self._jobs[job_id]["status"] = "failed"
            self._jobs[job_id]["error_message"] = f"Hugging Face generation failed: {str(e)}"

    async def generate(self, request: GenerationRequest) -> GenerationJob:
        """Submit a generation request to the background task."""
        job_id = f"hf-{uuid.uuid4().hex[:12]}"
        
        self._jobs[job_id] = {
            "status": "queued",
            "video_url": None,
            "error_message": None,
            "created_at": datetime.now(timezone.utc),
        }
        
        # Spawn the background task so we can return immediately
        asyncio.create_task(self._generate_task(job_id, request.prompt))
        
        return GenerationJob(provider_job_id=job_id, status="queued")

    async def get_status(self, provider_job_id: str) -> GenerationStatus:
        """Check the status of the background task."""
        job = self._jobs.get(provider_job_id)
        if not job:
            return GenerationStatus(
                status="failed",
                error_message="Job not found. The server may have restarted."
            )
            
        return GenerationStatus(
            status=job["status"],
            video_url=job["video_url"],
            error_message=job["error_message"]
        )

    @property
    def provider_name(self) -> str:
        return "huggingface"

    @property
    def model_name(self) -> str:
        return self.model
