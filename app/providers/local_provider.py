from typing import List
import json
import ctransformers
from pathlib import Path

from ..core.config import settings
from .base import LLMProvider


class LocalProvider(LLMProvider):
    def __init__(self):
        if not settings.LOCAL_MODEL_PATH:
            raise ValueError("LOCAL_MODEL_PATH must be set when using local provider")

        model_path = Path(settings.LOCAL_MODEL_PATH)
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")

        # Initialize the local model using ctransformers
        # This is just an example - you might want to use a different library
        # based on your specific needs (e.g., llama-cpp-python, transformers, etc.)
        self.llm = ctransformers.LLM(
            model_path=str(model_path),
            model_type="llama",  # adjust based on your model type
            config={
                "max_new_tokens": 512,
                "temperature": 0.7,
                "context_length": 2048,
            },
        )

    async def analyze_function(self, function_code: str) -> List[str]:
        """
        Analyze code using a locally hosted model.
        """
        prompt = f"""
        {self.SYSTEM_PROMPT}

        Function to analyze:
        ```python
        {function_code}
        ```
        """

        # Generate response from the local model
        response_text = self.llm(prompt)

        try:
            response_data = json.loads(response_text)
            return response_data.get("suggestions", [])
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            # Fallback: if JSON parsing fails, try to extract suggestions line by line
            return [
                s.strip()
                for s in response_text.split("\n")
                if s.strip()
                and not s.strip().startswith("{")
                and not s.strip().startswith("}")
            ]
