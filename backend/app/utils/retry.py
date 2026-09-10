"""Exponential backoff retry utility for transient failures.

Only retries on network errors and 5xx/429 status codes.
Never retries validation, auth, or client errors.
"""

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from app.core.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


async def retry_with_backoff(
    fn: Callable[..., Awaitable[T]],
    *args,
    max_retries: int = 3,
    base_delay: float = 1.0,
    retryable_exceptions: tuple[type[Exception], ...] = (
        ConnectionError,
        TimeoutError,
        OSError,
    ),
    **kwargs,
) -> T:
    """Execute an async function with exponential backoff on transient failures.

    Args:
        fn: The async function to execute.
        max_retries: Maximum number of retry attempts.
        base_delay: Initial delay in seconds (doubles each attempt).
        retryable_exceptions: Exception types that trigger a retry.

    Returns:
        The result of the function call.

    Raises:
        The last exception if all retries are exhausted.
    """
    last_exception: Exception | None = None

    for attempt in range(max_retries + 1):
        try:
            return await fn(*args, **kwargs)
        except retryable_exceptions as exc:
            last_exception = exc
            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                logger.warning(
                    "retry_attempt",
                    attempt=attempt + 1,
                    max_retries=max_retries,
                    delay_seconds=delay,
                    error=str(exc),
                )
                await asyncio.sleep(delay)
            else:
                logger.error(
                    "retry_exhausted",
                    attempts=max_retries + 1,
                    error=str(exc),
                )

    raise last_exception  # type: ignore[misc]
