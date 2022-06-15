from typing import Union
from redis import Redis
from fastapi import APIRouter, Depends, HTTPException
from backend.schemas import schemas
from backend import dal
import logging
from http import HTTPStatus


from backend.db.database import get_db  # type: ignore

from backend.celery import tasks
import pydantic

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/create", response_model=schemas.TaskOnlyHash, status_code=HTTPStatus.CREATED
)
def create_task(task: schemas.TaskIn, db: Redis = Depends(get_db)):  # type: ignore
    try:
        result = dal.create_task(db, task)  # type: ignore
    except pydantic.ValidationError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=e)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
    try:
        tasks.run_task(task_id=result.archive_hash, files=task.urls)  # type: ignore
    except Exception as e:
        logger.error(e)
        dal.change_task_status(db, str(result.archive_hash), schemas.Stages.ERROR)  # type: ignore
        raise HTTPException(status_code=500, detail=e)

    return result


@router.get(
    "/status/{archive_hash}",
    response_model=Union[schemas.TaskCompleted, schemas.TaskOnlyStatus],
)  # type: ignore
def get_task(archive_hash: str, db: Redis = Depends(get_db)):  # type: ignore
    try:
        result = dal.get_task(db=db, task_id=archive_hash)  # type: ignore
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=404, detail="Cannot find task with this id 🤷‍♂️"
        )
    return result
