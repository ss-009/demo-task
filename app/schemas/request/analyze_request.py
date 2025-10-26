from pydantic import BaseModel, Field, ConfigDict


class AnalyzeRequest(BaseModel):
    image_path: str = Field(
        ...,
        description="画像ファイルPath",
    )
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "image_path": "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg"
            }
        }
    )
