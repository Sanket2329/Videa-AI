"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.dependencies import get_db_session, get_current_user
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    summary="Register a new user",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED
)
async def register(
    request: UserCreate,
    session: AsyncSession = Depends(get_db_session),
) -> ApiResponse[UserResponse]:
    # Check if user exists
    result = await session.execute(select(User).where(User.email == request.email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    # Create new user
    hashed_password = get_password_hash(request.password)
    user = User(
        email=request.email,
        hashed_password=hashed_password,
        full_name=request.full_name
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    return ApiResponse.ok(UserResponse.model_validate(user, from_attributes=True))


@router.post(
    "/login",
    summary="Login and get access token",
    response_model=Token
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
) -> Token:
    # OAuth2PasswordRequestForm uses 'username' for the email/identifier
    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)


@router.get(
    "/me",
    summary="Get current user",
    response_model=ApiResponse[UserResponse]
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> ApiResponse[UserResponse]:
    return ApiResponse.ok(UserResponse.model_validate(current_user, from_attributes=True))
