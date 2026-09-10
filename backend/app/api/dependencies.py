"""FastAPI dependency injection wiring.

Provides service instances to route handlers via Depends().
The video generator is created once at startup and reused.
"""

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.db.session import get_db_session
from app.repositories.video import VideoRepository
from app.services.prompt.service import PromptService
from app.services.video.base import VideoGenerator
from app.services.video.factory import create_video_generator
from app.services.video.service import VideoService

# Cached video generator instance (created once, reused across requests)
_video_generator: VideoGenerator | None = None


def get_video_generator(
    settings: Settings = Depends(get_settings),
) -> VideoGenerator:
    """Get or create the singleton video generator."""
    global _video_generator
    if _video_generator is None:
        _video_generator = create_video_generator(settings)
    return _video_generator


def get_video_repository(
    session: AsyncSession = Depends(get_db_session),
) -> VideoRepository:
    """Create a VideoRepository scoped to the current request's DB session."""
    return VideoRepository(session)


def get_video_service(
    repository: VideoRepository = Depends(get_video_repository),
    generator: VideoGenerator = Depends(get_video_generator),
    settings: Settings = Depends(get_settings),
) -> VideoService:
    """Create a VideoService with all its dependencies."""
    return VideoService(
        repository=repository,
        generator=generator,
        settings=settings,
    )


def get_prompt_service(
    settings: Settings = Depends(get_settings),
) -> PromptService:
    """Create a PromptService."""
    return PromptService(settings=settings)


from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.models.user import User
from app.core.security import settings as security_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            security_settings.SECRET_KEY, 
            algorithms=[security_settings.ALGORITHM]
        )
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    from sqlalchemy import select
    import uuid
    
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise credentials_exception
        
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

