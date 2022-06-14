import aioredis
from backend.config import get_settings
from aioredis.client import Redis


async def get_db() -> Redis:
    settings = get_settings()
    return await aioredis.from_url(settings.redis_store_uri)  # type: ignore
