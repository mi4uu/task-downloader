import uvicorn
import os
from fastapi import FastAPI
import logging
from backend.config import get_settings
from backend.routers.main_router import router as main_router
from backend.routers.task_router import router as task_router
from fastapi.staticfiles import StaticFiles


logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
app = FastAPI()
settings = get_settings()

app.include_router(main_router)
app.include_router(task_router, prefix="/api/v1/task")

app.mount(
    settings.shared_storage_url,
    StaticFiles(directory=settings.shared_storage_url),
    name="storage",
)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
