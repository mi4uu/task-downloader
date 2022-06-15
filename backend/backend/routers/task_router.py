from redis import Redis
from fastapi import APIRouter, Depends, HTTPException
from backend.schemas import schemas
from backend import dal
import logging

from backend.db.database import get_db  # type: ignore

from backend.celery import tasks
import pydantic

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/")
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
        tasks.run_task(task_id=result.id, files=task.files)  # type: ignore
    except Exception as e:
        logger.error(e)
        dal.change_task_status(db, task.id, schemas.Stages.ERROR)
        raise HTTPException(status_code=500, detail=e)

    return result


@router.post("/{task_id}")
def get_task(task_id: str, db: Redis = Depends(get_db)):  # type: ignore
    try:
        result = dal.get_task(db, task_id)  # type: ignore
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=404, detail="Cannot find task with this id 🤷‍♂️"
        )
    return result
