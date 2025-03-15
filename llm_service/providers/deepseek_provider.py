from typing import List
import json
import httpx

from ..core.config import settings
from .base import LLMProvider


class DeepseekProvider(LLMProvider):
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.model = settings.DEEPSEEK_MODEL
        self.api_url = "https://api.deepseek.com/v1/chat/completions"  # Example URL, replace with actual Deepseek API endpoint

    async def analyze_function(self, function_code: str) -> List[str]:
        prompt = f"""
        Function to analyze:
        ```python
        {function_code}
        ```
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 500,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url, headers=headers, json=payload, timeout=30.0
            )
            response.raise_for_status()
            data = response.json()

            try:
                response_text = data["choices"][0]["message"]["content"]
                response_data = json.loads(response_text)
                return response_data.get("suggestions", [])
            except (json.JSONDecodeError, KeyError, AttributeError) as e:
                # Fallback: if JSON parsing fails, try to extract suggestions line by line
                suggestions_text = data["choices"][0]["message"]["content"]
                return [
                    s.strip()
                    for s in suggestions_text.split("\n")
                    if s.strip()
                    and not s.strip().startswith("{")
                    and not s.strip().startswith("}")
                ]
