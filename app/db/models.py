from sqlalchemy import Column, Integer, String, Boolean, Numeric
from app.db.database import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP


class AnalysisLog(Base):
    __tablename__ = "ai_analysis_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String(255), nullable=False)
    success = Column(Boolean, nullable=False)
    message = Column(String(255))
    class_ = Column("class", Integer, key="class_")
    confidence = Column(Numeric(5, 4))
    request_timestamp = Column(TIMESTAMP(precision=6, timezone=True))
    response_timestamp = Column(TIMESTAMP(precision=6, timezone=True))
