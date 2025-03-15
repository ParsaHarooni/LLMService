import pytest
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
@pytest.fixture(autouse=True)
def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    # If .env doesn't exist, we'll rely on the mocked values in tests
