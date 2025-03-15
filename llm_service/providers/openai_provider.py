from typing import List
import json
import openai
from openai import AsyncOpenAI

from ..core.config import settings
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def analyze_function(self, function_code: str) -> List[str]:
        prompt = f"""
        Function to analyze:
        ```python
        {function_code}
        ```
        """

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500,
            response_format={
                "type": "json_object"
            },  # Ensure JSON output for supported models
        )

        # Extract and parse JSON from the response
        try:
            response_text = response.choices[0].message.content
            response_data = json.loads(response_text)
            return response_data.get("suggestions", [])
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            # Fallback: if JSON parsing fails, try to extract suggestions line by line
            suggestions_text = response.choices[0].message.content
            return [
                s.strip()
                for s in suggestions_text.split("\n")
                if s.strip()
                and not s.strip().startswith("{")
                and not s.strip().startswith("}")
            ]
