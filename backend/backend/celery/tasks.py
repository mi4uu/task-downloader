# type: ignore
import json
from re import A
from typing import List
from backend.db.database import get_db
from backend.celery.worker import worker
from backend.schemas import schemas
from backend import dal
from asgiref.sync import async_to_sync
import logging
import celery
import os
from redis import Redis
import requests
from backend.config import get_settings
import shutil
import uuid


settings = get_settings()
logger = logging.getLogger(__name__)

db: Redis = get_db()


class Task(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"kwargs: {kwargs} args:{args}  task_id: {task_id}")
        error.delay(task_id=kwargs['task_id'] if 'task_id' in kwargs else args[0])

        logger.error('{0!r} failed: {1!r}'.format(task_id, exc))


@worker.task(base=Task)
def change_stage(task_id: str, stage: schemas.Stages) -> schemas.Task:
    results = dal.change_task_status(db, task_id, stage)
    return results.json()


@worker.task
def error(task_id: str):

    task = dal.change_task_status(db, task_id, schemas.Stages.ERROR)
    if task.callback_url:
        pingback.delay(task_id=task_id)

    return True


@worker.task(base=Task, bing=True)
def complete(self, task_id: str):

    task = dal.complete_task(db, task_id)
    if task.callback_url:
        pingback.delay(task_id=task_id)

    return self


@worker.task(base=Task)
def download_file(task_id: str, url: str):
    response = requests.get(url, stream=True)

    basename = (
        os.path.basename((url))
        or url.split("/")[-1]
        or url.split("/")[-2]
        or str(uuid.uuid4())
    )

    directory = os.path.join(os.path.join(settings.shared_storage_url, task_id))
    filename = os.path.join(directory, basename)

    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename, "wb") as handle:
        for data in response.iter_content():
            handle.write(data)
    return True


@worker.task(base=Task)
def create_archive(self, task_id: str):
    directory = os.path.join(os.path.join(settings.shared_storage_url, task_id))
    shutil.make_archive(directory, 'zip', directory)
    return True


@worker.task()
def pingback(task_id: str):
    task = dal.get_task(db, task_id)
    requests.get(task.callback_url, json=task.json())


def run_task(task_id: str, files: List[str]):
    change_stage.delay(task_id=task_id, stage=schemas.Stages.RUNNING)
    mark_as_complete_task = complete.s(task_id=task_id)
    create_archive_task = create_archive.s(task_id=task_id)
    g = celery.group([download_file.s(task_id, file) for file in files])

    celery.chain(g, create_archive_task, mark_as_complete_task).delay()

    return True
