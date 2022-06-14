from datetime import datetime
import uuid
from aioredis import Redis
from backend.schemas import schemas


async def create_task(db: Redis, task: schemas.TaskIn) -> schemas.Task:

    task_id = uuid.uuid4()
    new_task = schemas.Task(id=task_id, created_at=datetime.now(), **task.dict())

    result = await db.set(str(task_id), new_task.json())  # type: ignore
    if result:
        return new_task
    raise Exception("Failed to create task")


async def change_task_status(db: Redis, task_id: str, new_status: schemas.Stages) -> schemas.Task:

    task_data = await db.get(task_id)  # type: ignore

    task = schemas.Task.parse_raw(task_data)
    task.status = new_status
    task.updated_at = datetime.now()

    result = await db.set(task_id, task.json())  # type: ignore
    if result:
        return task
    raise Exception("Failed to create task")
