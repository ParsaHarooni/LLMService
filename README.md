# LLM Service (AI Gateway)

A FastAPI-based microservice that acts as a gateway to various LLM providers for code analysis.

## Features

- Support for multiple LLM providers (OpenAI, Deepseek, Local)
- Provider selection via environment variables
- Code analysis endpoint with standardized response format
- FastAPI with async support
- Comprehensive test suite
- Type checking with mypy
- Code formatting with black
- Linting with pylint

## Setup

1. Install Poetry (package manager):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Copy the environment file and configure your settings:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your API keys and preferences.

## Running the Service

1. Start the service:
   ```bash
   poetry run uvicorn llm_service.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`
   - API documentation: `http://localhost:8000/docs`
   - OpenAPI spec: `http://localhost:8000/openapi.json`

## Usage

Send a POST request to `/api/v1/analyze` with your code:

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"function_code": "def add(a, b): return a + b"}'
```

## Running Tests

```bash
poetry run pytest
```

## Development

- Format code:
  ```bash
  poetry run black .
  ```

- Type checking:
  ```bash
  poetry run mypy .
  ```

- Linting:
  ```bash
  poetry run pylint llm_service
  ```

## Environment Variables

- `LLM_PROVIDER`: Choose the LLM provider (`openai`, `deepseek`, or `local`)
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-3.5-turbo)
- `DEEPSEEK_API_KEY`: Your Deepseek API key (if using Deepseek)
- `DEEPSEEK_MODEL`: Deepseek model to use
- `LOCAL_MODEL_PATH`: Path to local model (if using local provider)

## Project Structure

```
llm_service/
├── api/
│   ├── models.py      # Pydantic models
│   └── router.py      # FastAPI router
├── core/
│   └── config.py      # Configuration and settings
├── providers/
│   ├── base.py        # Base provider interface
│   └── openai_provider.py  # OpenAI implementation
└── main.py            # FastAPI application
``` 