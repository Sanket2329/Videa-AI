"""Common API response schemas.

All API responses use the ApiResponse wrapper for consistency.
Success responses carry data in the `data` field; error responses
carry structured error info in the `error` field.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Structured error information returned to clients."""
    code: str
    message: str


class ApiResponse(BaseModel, Generic[T]):
    """Consistent API response wrapper used by all endpoints."""
    success: bool
    data: T | None = None
    error: ErrorDetail | None = None

    @classmethod
    def ok(cls, data: T) -> "ApiResponse[T]":
        """Create a successful response."""
        return cls(success=True, data=data, error=None)

    @classmethod
    def fail(cls, code: str, message: str) -> "ApiResponse[None]":
        """Create an error response."""
        return cls(success=False, data=None, error=ErrorDetail(code=code, message=message))
