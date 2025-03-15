from pydantic import BaseModel, ConfigDict
from typing import List


class AnalyzeRequest(BaseModel):
    function_code: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"function_code": "def add(a, b): return a + b"}}
    )


class AnalyzeResponse(BaseModel):
    suggestions: List[str]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "suggestions": [
                    "Consider adding type hints.",
                    "Add a docstring for better documentation.",
                ]
            }
        }
    )
