from celery import Celery
from backend.config import get_settings

settings = get_settings()

worker: Celery = Celery('hello', broker=settings.broker_uri, backend=settings.backend_uri)
