from abc import ABC, abstractmethod
from typing import List, ClassVar


class LLMProvider(ABC):
    # Common configuration for all providers
    SYSTEM_PROMPT: ClassVar[
        str
    ] = """You are a Python code review expert. Your task is to analyze Python code and provide suggestions for improvement.
Focus on:
- Code quality and best practices
- Type hints and type safety
- Documentation and readability
- Performance considerations
- Security implications

Provide your suggestions in JSON format with the following structure:
{
    "suggestions": [
        "suggestion 1",
        "suggestion 2",
        ...
    ]
}

Include only the JSON in your response, no other text."""

    @abstractmethod
    async def analyze_function(self, function_code: str) -> List[str]:
        """
        Analyze the given function code and return a list of suggestions.

        Args:
            function_code: The Python function code to analyze

        Returns:
            List of suggestions for improving the code
        """
        pass
