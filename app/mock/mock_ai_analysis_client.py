import random


class MockAiAnalysisClient:
    def __init__(self, succeed=True):
        self.succeed = succeed

    async def analyze_image(self, image_path: str) -> dict:
        if self.succeed:
            return {
                "success": True,
                "message": "success",
                "estimated_data": {
                    "class": random.randint(1, 5),
                    "confidence": round(random.uniform(0.0, 0.99), 4),
                },
            }
        else:
            return {
                "success": False,
                "message": "Error:E50012",
                "estimated_data": {},
            }
