import pytest
from unittest.mock import AsyncMock
from app.services.analysis_service import AnalysisService
from app.mock.mock_ai_analysis_client import MockAiAnalysisClient
from app.schemas.response.analyze_response import AnalyzeResponse, EstimatedData


@pytest.mark.asyncio
async def test_analyze_and_save_success():
    """正常系: API成功, Repository保存成功"""
    mock_client = MockAiAnalysisClient()
    mock_repo = AsyncMock()
    service = AnalysisService(mock_client, mock_repo)
    response = await service.analyze_and_save("/image/test_success.jpg", session=None)

    assert isinstance(response, AnalyzeResponse)
    assert response.success is True
    assert isinstance(response.estimated_data.class_, int)
    assert isinstance(response.estimated_data.confidence, float)
    mock_repo.save_analysis_result.assert_called_once()


@pytest.mark.asyncio
async def test_analyze_and_save_api_failure():
    """API失敗時: Serviceは success=False"""
    mock_client = MockAiAnalysisClient(succeed=False)
    mock_repo = AsyncMock()
    service = AnalysisService(mock_client, mock_repo)
    response = await service.analyze_and_save("/image/test_fail.jpg", session=None)
    assert response.success is False
    assert response.message == "Error:E50012"
    assert isinstance(response.estimated_data, EstimatedData)
    mock_repo.save_analysis_result.assert_called_once()


@pytest.mark.asyncio
async def test_analyze_and_save_db_failure():
    """Repository保存失敗時: Serviceは例外をcatch、レスポンスは正常系と同じ"""
    mock_client = MockAiAnalysisClient(succeed=True)

    class FailingRepo:
        async def save_analysis_result(*args, **kwargs):
            raise Exception("DB Error")

    service = AnalysisService(mock_client, FailingRepo())
    response = await service.analyze_and_save("/image/test_db_fail.jpg", session=None)

    assert response.success is True
    assert response.message == "success"
    assert isinstance(response.estimated_data.class_, int)
    assert isinstance(response.estimated_data.confidence, float)
