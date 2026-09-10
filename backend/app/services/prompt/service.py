"""PromptService — orchestrates prompt validation and enhancement.

Validates prompt constraints, delegates to the LLM enhancer, and
falls back gracefully to the original prompt if enhancement fails.
"""

from app.core.config import Settings
from app.core.exceptions import EmptyPromptError, PromptTooLongError
from app.core.logging import get_logger
from app.schemas.prompt import EnhancedPromptData, PromptEnhanceResponse
from app.services.prompt.enhancer import PromptEnhancer

logger = get_logger(__name__)


class PromptService:
    """Prompt validation and enhancement."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._enhancer = PromptEnhancer(settings)

    def validate_prompt(self, prompt: str) -> str:
        """Validate and clean a user prompt.

        Returns the trimmed prompt.
        Raises EmptyPromptError or PromptTooLongError on failure.
        """
        cleaned = prompt.strip()
        if not cleaned:
            raise EmptyPromptError()
        if len(cleaned) > self._settings.MAX_PROMPT_LENGTH:
            raise PromptTooLongError(self._settings.MAX_PROMPT_LENGTH)
        return cleaned

    async def enhance_prompt(
        self, prompt: str, style: str = "cinematic"
    ) -> PromptEnhanceResponse:
        """Enhance a prompt using the LLM, with graceful fallback.

        If the LLM fails, returns a response using the original prompt
        as the enhanced_prompt, with empty supplementary fields.
        """
        cleaned = self.validate_prompt(prompt)

        result = await self._enhancer.enhance(cleaned, style)

        if result is not None:
            return PromptEnhanceResponse(
                original_prompt=cleaned,
                enhanced_prompt=result.enhanced_prompt,
                negative_prompt=result.negative_prompt,
                camera=result.camera,
                lighting=result.lighting,
                style=result.style,
                motion=result.motion,
            )

        # Graceful fallback: use original prompt
        logger.info(
            "prompt_enhancement_fallback",
            reason="LLM enhancement returned None",
            prompt_length=len(cleaned),
        )
        return PromptEnhanceResponse(
            original_prompt=cleaned,
            enhanced_prompt=cleaned,
            negative_prompt="blur, distort, low quality, watermark, text",
            camera="",
            lighting="",
            style=style,
            motion="",
        )
