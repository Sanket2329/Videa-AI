import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_enhance_prompt_success(client: AsyncClient):
    with patch("app.services.prompt.enhancer.PromptEnhancer.enhance") as mock_enhance:
        # Mock the LLM response
        mock_response = MagicMock()
        mock_response.enhanced_prompt = "An enhanced, cinematic shot of a testing scene"
        mock_response.negative_prompt = "blur, low quality"
        mock_response.camera = "Slow pan"
        mock_response.lighting = "Dramatic"
        mock_response.style = "Cinematic"
        mock_response.motion = "Slow motion"
        mock_enhance.return_value = mock_response

        response = await client.post("/prompts/enhance", json={
            "prompt": "A simple test",
            "style": "cinematic"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["original_prompt"] == "A simple test"
        assert data["data"]["enhanced_prompt"] == "An enhanced, cinematic shot of a testing scene"

@pytest.mark.asyncio
async def test_enhance_prompt_fallback(client: AsyncClient):
    with patch("app.services.prompt.enhancer.PromptEnhancer.enhance") as mock_enhance:
        # Simulate LLM failure by returning None
        mock_enhance.return_value = None

        response = await client.post("/prompts/enhance", json={
            "prompt": "Fallback test",
            "style": "anime"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["original_prompt"] == "Fallback test"
        # On fallback, enhanced prompt matches original
        assert data["data"]["enhanced_prompt"] == "Fallback test"
        assert "blur" in data["data"]["negative_prompt"]
