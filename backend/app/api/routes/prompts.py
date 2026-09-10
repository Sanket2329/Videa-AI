"""Prompt enhancement API route."""

from fastapi import APIRouter, Depends

from app.api.dependencies import get_prompt_service
from app.schemas.common import ApiResponse
from app.schemas.prompt import PromptEnhanceRequest, PromptEnhanceResponse
from app.services.prompt.service import PromptService

router = APIRouter(prefix="/prompts", tags=["Prompts"])


@router.post(
    "/enhance",
    summary="Enhance a prompt",
    description=(
        "Transform a basic text description into a structured, cinematic, "
        "video-generation-ready prompt using an LLM. Falls back to the "
        "original prompt if enhancement fails."
    ),
    response_model=ApiResponse[PromptEnhanceResponse],
)
async def enhance_prompt(
    request: PromptEnhanceRequest,
    service: PromptService = Depends(get_prompt_service),
) -> ApiResponse[PromptEnhanceResponse]:
    result = await service.enhance_prompt(
        prompt=request.prompt,
        style=request.style,
    )
    return ApiResponse.ok(result)
