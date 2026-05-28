import os

import pytest
from starlette.testclient import TestClient

# Set test database before importing app
os.environ["DB_URL"] = os.getenv("DB_URL", "sqlite:///./test.db")

from app.main import app


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client
