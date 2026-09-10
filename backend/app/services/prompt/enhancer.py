"""LLM-based prompt enhancement using Google Gemini.

Transforms basic user prompts into structured, cinematic, video-
generation-ready prompts while preserving the user's original intent.
Falls back gracefully to the original prompt if enhancement fails.
"""

import json

import google.generativeai as genai

from app.core.config import Settings
from app.core.logging import get_logger
from app.schemas.prompt import EnhancedPromptData

logger = get_logger(__name__)

SYSTEM_PROMPT = """You are an expert video production director specializing in AI-generated video.

Given a user's text description and a style preset, produce a structured JSON response
that enhances the prompt for optimal text-to-video generation.

RULES:
1. Preserve the user's original subject and action — never change what they asked for.
2. Preserve any explicitly mentioned environment or setting.
3. Add cinematographic details: camera movement, lens, composition.
4. Add appropriate lighting based on the style.
5. Add motion description that fits the scene.
6. Avoid contradictions (e.g., "static shot" + "fast camera pan").
7. Keep enhanced_prompt under 500 characters.
8. negative_prompt: list things to avoid (blur, low quality, text, watermarks).
9. Do NOT add random or excessive details that weren't implied by the user.

STYLE GUIDELINES:
- cinematic: dramatic lighting, depth of field, anamorphic lens, controlled dolly/crane movement
- realistic: natural lighting, documentary-style, handheld subtle movement, real-world textures
- anime: anime art style, vibrant colors, cel shading, dynamic action poses
- 3d: 3D rendered, CGI quality, volumetric lighting, smooth camera orbit
- product: studio lighting, premium product photography, controlled rotation, reflections, luxury aesthetic

Return ONLY valid JSON matching this exact schema (no markdown, no extra text):
{
  "enhanced_prompt": "The full enhanced prompt text",
  "negative_prompt": "Things to avoid",
  "camera": "Camera movement and lens description",
  "lighting": "Lighting setup description",
  "style": "Visual style description",
  "motion": "Motion and movement description"
}"""


class PromptEnhancer:
    """Enhances user prompts using Google Gemini."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model_name = settings.GEMINI_MODEL

        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)

    async def enhance(self, prompt: str, style: str = "cinematic") -> EnhancedPromptData | None:
        """Enhance a user prompt using the LLM.

        Returns an EnhancedPromptData object on success, or None on failure.
        Failures are logged but never propagated — the caller should fall back
        to the original prompt.
        """
        if not self._settings.GEMINI_API_KEY:
            logger.warning("llm_enhancement_skipped", reason="No GEMINI_API_KEY configured")
            return None

        try:
            model = genai.GenerativeModel(
                model_name=self._settings.GEMINI_MODEL,
                system_instruction=SYSTEM_PROMPT,
            )

            user_message = f"Style: {style}\nPrompt: {prompt}"

            response = model.generate_content(
                user_message,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1024,
                    response_mime_type="application/json",
                ),
            )

            if not response.text:
                logger.warning("llm_empty_response", prompt_length=len(prompt))
                return None

            # Parse and validate the JSON response
            raw_text = response.text.strip()
            # Remove markdown code fences if present
            if raw_text.startswith("```"):
                raw_text = raw_text.split("\n", 1)[1] if "\n" in raw_text else raw_text[3:]
                if raw_text.endswith("```"):
                    raw_text = raw_text[:-3]
                raw_text = raw_text.strip()

            data = json.loads(raw_text)
            enhanced = EnhancedPromptData.model_validate(data)

            logger.info(
                "prompt_enhanced",
                original_length=len(prompt),
                enhanced_length=len(enhanced.enhanced_prompt),
                style=style,
            )
            return enhanced

        except json.JSONDecodeError as exc:
            logger.warning(
                "llm_invalid_json",
                error=str(exc),
                prompt_length=len(prompt),
            )
            return None
        except Exception as exc:
            logger.warning(
                "llm_enhancement_failed",
                error=str(exc),
                error_type=type(exc).__name__,
                prompt_length=len(prompt),
            )
            return None
