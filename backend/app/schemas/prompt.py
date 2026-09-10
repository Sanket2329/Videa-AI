"""Pydantic schemas for prompt enhancement."""

from pydantic import BaseModel, Field


class PromptEnhanceRequest(BaseModel):
    """Request to enhance a user prompt via LLM."""
    prompt: str = Field(..., min_length=1, max_length=2000, description="The user's raw prompt")
    style: str = Field(
        default="cinematic",
        pattern="^(cinematic|realistic|anime|3d|product)$",
        description="Style preset to guide enhancement",
    )


class EnhancedPromptData(BaseModel):
    """Structured LLM response for prompt enhancement."""
    enhanced_prompt: str = Field(..., description="The enhanced, video-generation-ready prompt")
    negative_prompt: str = Field(..., description="Things to avoid in generation")
    camera: str = Field(..., description="Camera movement and lens description")
    lighting: str = Field(..., description="Lighting setup description")
    style: str = Field(..., description="Visual style description")
    motion: str = Field(..., description="Motion and movement description")


class PromptEnhanceResponse(BaseModel):
    """Full response for the prompt enhancement endpoint."""
    original_prompt: str
    enhanced_prompt: str
    negative_prompt: str
    camera: str
    lighting: str
    style: str
    motion: str
