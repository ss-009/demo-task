from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.request.analyze_request import AnalyzeRequest
from app.schemas.response.analyze_response import AnalyzeResponse
from app.services.analysis_service import AnalysisService
from app.mock.mock_ai_analysis_client import MockAiAnalysisClient
from app.repositories.analysis_repository import AnalysisRepository
from app.db.database import get_session

analysis_router = APIRouter()
service = AnalysisService(MockAiAnalysisClient(), AnalysisRepository())


@analysis_router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_image(
    request: AnalyzeRequest, session: AsyncSession = Depends(get_session)
):
    return await service.analyze_and_save(request.image_path, session)
