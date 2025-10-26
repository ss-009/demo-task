from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AnalysisLog
from datetime import datetime
from app.schemas.response.analyze_response import AnalyzeResponse


class AnalysisRepository:
    async def save_analysis_result(
        self,
        session: AsyncSession,
        image_path: str,
        api_response: AnalyzeResponse,
        request_ts: datetime,
        response_ts: datetime,
    ):
        try:
            record = AnalysisLog(
                image_path=image_path,
                success=api_response.success,
                message=api_response.message,
                class_=api_response.estimated_data.class_,
                confidence=api_response.estimated_data.confidence,
                request_timestamp=request_ts,
                response_timestamp=response_ts,
            )
            session.add(record)
            await session.commit()
            await session.refresh(record)
        except Exception:
            await session.rollback()
            raise
        return record
