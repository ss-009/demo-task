import pytest


@pytest.mark.asyncio
async def test_analyze_endpoint(client):
    payload = {"image_path": "/image/test_controller.jpg"}
    response = client.post("/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "message" in data
    assert "estimated_data" in data
    assert "class" in data["estimated_data"] or "class_" in data["estimated_data"]
    assert "confidence" in data["estimated_data"]
