import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"

@pytest.mark.asyncio
async def test_generate_video_success(client: AsyncClient):
    response = await client.post("/videos/generate", json={
        "prompt": "A test video prompt",
        "style": "cinematic",
        "aspect_ratio": "16:9",
        "duration": 5
    })
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "queued"
    assert data["data"]["original_prompt"] == "A test video prompt"
    
    video_id = data["data"]["id"]
    
    # Check status
    status_response = await client.get(f"/videos/{video_id}")
    assert status_response.status_code == 200
    
    # Check history
    history_response = await client.get("/videos/history")
    assert history_response.status_code == 200
    assert len(history_response.json()["data"]) >= 1

@pytest.mark.asyncio
async def test_generate_video_validation_error(client: AsyncClient):
    # Missing required field
    response = await client.post("/videos/generate", json={
        "style": "cinematic",
    })
    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_generate_video_invalid_style(client: AsyncClient):
    response = await client.post("/videos/generate", json={
        "prompt": "Test",
        "style": "invalid_style",
    })
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_delete_video(client: AsyncClient):
    # Create
    create_resp = await client.post("/videos/generate", json={
        "prompt": "To be deleted",
        "style": "cinematic",
        "aspect_ratio": "16:9",
        "duration": 5
    })
    video_id = create_resp.json()["data"]["id"]
    
    # Delete
    del_resp = await client.delete(f"/videos/{video_id}")
    assert del_resp.status_code == 200
    
    # Verify deleted
    get_resp = await client.get(f"/videos/{video_id}")
    assert get_resp.status_code == 404
