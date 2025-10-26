import pytest
from datetime import datetime, timezone
from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.response.analyze_response import AnalyzeResponse, EstimatedData
from app.db.models import AnalysisLog
from app.tests.conftest import AsyncSessionLocal


@pytest.mark.asyncio
async def test_save_analysis_result():
    repo = AnalysisRepository()
    async with AsyncSessionLocal() as session:
        request_ts = datetime.now(timezone.utc)
        response = AnalyzeResponse(
            success=True,
            message="success",
            estimated_data=EstimatedData(**{"class": 3, "confidence": 0.8683}),
        )
        record: AnalysisLog = await repo.save_analysis_result(
            session=session,
            image_path="/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg",
            api_response=response,
            request_ts=request_ts,
            response_ts=datetime.now(timezone.utc),
        )

        assert record.id is not None
        assert (
            record.image_path
            == "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg"
        )
        assert record.success is True
        assert record.message == "success"
        assert record.class_ == 3
        assert float(record.confidence) == 0.8683
