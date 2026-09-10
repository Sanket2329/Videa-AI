"""Video generation API routes.

Handles the full generation lifecycle:
  POST   /generate  — Submit a new generation job
  GET    /{id}      — Check status (triggers lazy provider check)
  GET    /history   — List recent generations
  DELETE /{id}      — Remove a generation record
"""

import uuid

from fastapi import APIRouter, Depends

from app.api.dependencies import get_video_service, get_current_user
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.video import (
    VideoDeleteResponse,
    VideoGenerateRequest,
    VideoResponse,
)
from app.services.video.service import VideoService

router = APIRouter(prefix="/videos", tags=["Videos"])


@router.post(
    "/generate",
    summary="Generate a video",
    description=(
        "Submit a video generation request. Returns immediately with a job ID "
        "and 'queued' status. Poll GET /videos/{id} to track progress."
    ),
    response_model=ApiResponse[VideoResponse],
    status_code=201,
)
async def generate_video(
    request: VideoGenerateRequest,
    service: VideoService = Depends(get_video_service),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[VideoResponse]:
    video = await service.create_generation(
        prompt=request.prompt,
        enhanced_prompt=request.enhanced_prompt,
        negative_prompt=request.negative_prompt,
        style=request.style.value,
        aspect_ratio=request.aspect_ratio.value,
        duration=request.duration.value,
        user_id=current_user.id,
    )
    response = VideoResponse.model_validate(video, from_attributes=True)
    return ApiResponse.ok(response)


@router.get(
    "/history",
    summary="Get generation history",
    description="Return the 5 most recent video generations for the current user.",
    response_model=ApiResponse[list[VideoResponse]],
)
async def get_history(
    service: VideoService = Depends(get_video_service),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[VideoResponse]]:
    videos = await service.get_history(user_id=current_user.id, limit=5)
    responses = []
    for v in videos:
        resp = VideoResponse.model_validate(v, from_attributes=True)
        responses.append(resp)
    return ApiResponse.ok(responses)


@router.get(
    "/{video_id}",
    summary="Get video status",
    description=(
        "Get the current status of a video generation. If the generation "
        "is still active, this triggers a lazy status check with the provider."
    ),
    response_model=ApiResponse[VideoResponse],
)
async def get_video(
    video_id: uuid.UUID,
    service: VideoService = Depends(get_video_service),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[VideoResponse]:
    video = await service.get_generation(video_id, user_id=current_user.id)
    response = VideoResponse.model_validate(video, from_attributes=True)
    return ApiResponse.ok(response)


@router.delete(
    "/{video_id}",
    summary="Delete a video",
    description="Remove a video generation record from history.",
    response_model=ApiResponse[VideoDeleteResponse],
)
async def delete_video(
    video_id: uuid.UUID,
    service: VideoService = Depends(get_video_service),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[VideoDeleteResponse]:
    await service.delete_generation(video_id, user_id=current_user.id)
    return ApiResponse.ok(VideoDeleteResponse(deleted=True))
