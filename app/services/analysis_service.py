from datetime import datetime
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.mock.mock_ai_analysis_client import MockAiAnalysisClient
from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.response.analyze_response import AnalyzeResponse, EstimatedData
from app.constants.response import ErrorMessages
from app.constants.timezone import JST


class AnalysisService:
    def __init__(
        self,
        mock_ai_analysis_client: MockAiAnalysisClient,
        repository: AnalysisRepository,
    ):
        self.mock_ai_analysis_client = mock_ai_analysis_client
        self.repository = repository

    async def analyze_and_save(
        self, image_path: str, session: AsyncSession
    ) -> AnalyzeResponse:
        request_ts = datetime.now(JST)
        try:
            response_api = await self._call_ai_api(image_path)
            response = AnalyzeResponse(**response_api)
        except Exception as e:
            print(f"{ErrorMessages.ERROR_ANALYZE_IMAGE}: {e}")
            response = AnalyzeResponse(
                success=False,
                message=ErrorMessages.ERROR_E50012,
                estimated_data=EstimatedData(),
            )
        await self._save_to_db(session, image_path, response, request_ts)
        return response

    async def _call_ai_api(self, image_path: str) -> Dict:
        try:
            return await self.mock_ai_analysis_client.analyze_image(image_path)
        except Exception as e:
            print(f"{ErrorMessages.ERROR_ANALYZE_IMAGE}: {e}")
            return {
                "success": False,
                "message": ErrorMessages.ERROR_E50012,
                "estimated_data": {},
            }

    async def _save_to_db(
        self,
        session: AsyncSession,
        image_path: str,
        response: AnalyzeResponse,
        request_ts: datetime,
    ):
        try:
            response_ts = datetime.now(JST)
            await self.repository.save_analysis_result(
                session, image_path, response, request_ts, response_ts
            )
        except Exception as e:
            print(f"{ErrorMessages.ERROR_INSERT_AI_ANALYSIS_LOG}: {e}")
