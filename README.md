# LLM Service

A FastAPI-based service that provides code analysis using various LLM providers (OpenAI, Deepseek, and Local models).

## Features

- Multiple LLM provider support (OpenAI, Deepseek, Local)
- FastAPI-based REST API
- JSON-formatted code analysis suggestions
- Comprehensive test suite
- Type checking and linting

## Requirements

- Python 3.11+
- Poetry for dependency management
- Nox for automation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd llm-service
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
poetry install
```

4. Create a `.env` file with your configuration:
```bash
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_MODEL=deepseek-chat-v3
LOCAL_MODEL_PATH=/path/to/local/model  # Optional
```

## Development

We use Nox for automating development tasks. Here are the available sessions:

### Running Tests

```bash
# Run all tests
nox -s tests

# Run a specific test file
nox -s tests -- tests/test_api.py

# Run a specific test function
nox -s tests -- tests/test_api.py::test_analyze_endpoint
```

### Code Quality

```bash
# Run linting (black)
nox -s lint

# Run type checking (mypy)
nox -s type_check
```

### Running All Sessions

```bash
# Run all Nox sessions
nox
```

## API Usage

Start the server:
```bash
poetry run uvicorn llm_service.main:app --reload
```

Example API request:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"function_code": "def add(a, b): return a + b"}'
```

## Project Structure

```
llm_service/
├── api/            # API endpoints and models
├── core/           # Core configuration
├── providers/      # LLM provider implementations
└── tests/          # Test suite
```
