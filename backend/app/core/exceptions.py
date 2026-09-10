"""Custom exception hierarchy for the application.

These exceptions are caught by FastAPI exception handlers in main.py
and translated into consistent API error responses. Internal details
(stack traces, provider errors) are logged but never exposed to clients.
"""


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class ValidationError(AppException):
    """Raised when request validation fails beyond Pydantic checks."""

    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        super().__init__(message=message, code=code, status_code=422)


class PromptTooLongError(ValidationError):
    """Raised when the prompt exceeds the maximum allowed length."""

    def __init__(self, max_length: int):
        super().__init__(
            message=f"Your prompt is too long. Please shorten it to under {max_length} characters.",
            code="PROMPT_TOO_LONG",
        )


class EmptyPromptError(ValidationError):
    """Raised when the prompt is empty or whitespace-only."""

    def __init__(self):
        super().__init__(
            message="Please enter a description for your video.",
            code="EMPTY_PROMPT",
        )


class GenerationError(AppException):
    """Raised when video generation fails."""

    def __init__(self, message: str = "Video generation failed. Please try again."):
        super().__init__(message=message, code="GENERATION_FAILED", status_code=500)


class GenerationTimeoutError(AppException):
    """Raised when video generation exceeds the timeout."""

    def __init__(self):
        super().__init__(
            message="Generation is taking longer than expected. Please retry or check the generation history.",
            code="GENERATION_TIMEOUT",
            status_code=504,
        )


class ProviderError(AppException):
    """Raised when the video/LLM provider returns an error."""

    def __init__(self, message: str = "The AI service encountered an error. Please try again."):
        super().__init__(message=message, code="PROVIDER_ERROR", status_code=502)


class RateLimitError(AppException):
    """Raised when rate limits are exceeded."""

    def __init__(self):
        super().__init__(
            message="The AI service is temporarily busy. Please try again shortly.",
            code="RATE_LIMITED",
            status_code=429,
        )


class NotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(
            message=f"{resource} not found.",
            code="NOT_FOUND",
            status_code=404,
        )


class DuplicateGenerationError(AppException):
    """Raised when a duplicate generation request is detected."""

    def __init__(self):
        super().__init__(
            message="A generation request is already in progress. Please wait for it to complete.",
            code="DUPLICATE_GENERATION",
            status_code=409,
        )
