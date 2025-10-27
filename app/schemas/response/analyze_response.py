from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class EstimatedData(BaseModel):
    class_: Optional[int] = Field(None, alias="class", description="分類されたクラスID")
    confidence: Optional[float] = Field(None, description="分類の確信度（0.0〜1.0）")

    model_config = ConfigDict(
        json_schema_extra={"example": {"class": 3, "confidence": 0.8683}}
    )


class AnalyzeResponse(BaseModel):
    success: bool = Field(..., description="操作が成功したか")
    message: str = Field(..., description="操作の結果メッセージ")
    estimated_data: EstimatedData = Field(
        default_factory=EstimatedData, description="解析結果の詳細"
    )

    model_config: ConfigDict = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "success",
                "estimated_data": {"class": 3, "confidence": 0.8683},
            }
        }
    )
