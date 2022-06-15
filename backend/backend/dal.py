from datetime import datetime
import uuid
from redis import Redis
from backend.schemas import schemas


def create_task(db: Redis, task: schemas.TaskIn) -> schemas.Task:  # type: ignore

    task_id = uuid.uuid4()
    new_task = schemas.Task(
        archive_hash=task_id,
        created_at=datetime.now(),
        modified_at=datetime.now(),
        **task.dict(),
    )

    result = db.set(str(task_id), new_task.json())  # type: ignore
    if result:
        return new_task
    raise Exception("Failed to create task")


def change_task_status(db: Redis, task_id: str, new_status: schemas.Stages) -> schemas.Task:  # type: ignore

    task_data = db.get(task_id)  # type: ignore

    task: schemas.Task = schemas.Task.parse_raw(task_data)  # type: ignore
    task.status = new_status
    task.modified_at = datetime.now()

    result = db.set(task_id, task.json())  # type: ignore
    if result:
        return task
    raise Exception("Failed to change task")


def complete_task(db: Redis, task_id: str) -> schemas.Task:  # type: ignore

    task_data = db.get(task_id)  # type: ignore

    task: schemas.Task = schemas.Task.parse_raw(task_data)  # type: ignore
    task.url = f"http://localhost:8080/storage/{task_id}.zip"
    task.status = schemas.Stages.COMPLETED
    task.modified_at = datetime.now()

    result = db.set(task_id, task.json())  # type: ignore
    if result:
        return task
    raise Exception("Failed to change task")


def get_task(db: Redis, task_id: str) -> schemas.Task:  # type: ignore

    task_data = db.get(task_id)  # type: ignore

    task = schemas.Task.parse_raw(task_data)  # type: ignore
    return task
