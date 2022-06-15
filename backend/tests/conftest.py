from httpx import AsyncClient
import pytest
from backend.main import app

client_ = AsyncClient(app=app, base_url="http://test")  # type: ignore


@pytest.fixture()
def client():
    return client_
