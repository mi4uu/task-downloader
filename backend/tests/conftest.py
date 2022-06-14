import os

from backend.db.database import get_db

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@database/test"
os.environ["SQLALCHEMY_DATABASE_URL"] = SQLALCHEMY_DATABASE_URL
import logging
from backend.db.models import BaseModel
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # type: ignore
from sqlalchemy.orm import sessionmaker
from typing import AsyncIterable
from backend.main import app
from fastapi.testclient import TestClient
from backend.config import AppSettings, get_settings
from httpx import AsyncClient

logger = logging.getLogger(__name__)


def override_get_settings() -> AppSettings:
    conf = AppSettings()
    conf.database_url = SQLALCHEMY_DATABASE_URL
    # conf.shared_storage_url = "/tmp/"

    return conf


async def override_get_db() -> AsyncIterable[AsyncSession]:
    Engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        future=True,
        echo=True,
    )
    SessionLocal = sessionmaker(Engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore
    db: AsyncSession = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def init_models():
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        future=True,
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)  # type: ignore
        logger.info("Dropped all tables")
        await conn.run_sync(BaseModel.metadata.create_all)  # type: ignore
        logger.info("Created all tables")

    await engine.dispose()


@pytest_asyncio.fixture  # type: ignore
async def test_db():
    logger.info("INITIALIZING DB")

    await init_models()
    return await override_get_db().__anext__()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_settings] = override_get_settings


client_ = TestClient(app)  # type: ignore
client_ = AsyncClient(app=app, base_url="http://test")  # type: ignore


@pytest.fixture()
def client():
    return client_


@pytest.fixture()
def get_settings():
    return override_get_settings()
