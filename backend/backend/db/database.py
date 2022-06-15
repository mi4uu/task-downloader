from backend.config import get_settings
from redis import Redis


def get_db() -> Redis:  # type: ignore
    settings = get_settings()
    return Redis.from_url(settings.redis_store_uri)  # type: ignore
