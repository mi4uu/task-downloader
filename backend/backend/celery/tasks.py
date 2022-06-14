from backend.db.database import get_db
from backend.celery.worker import worker

db = get_db()


@worker.task
def move_to_next_stage(name: str, stage: str):
    db.set(name, stage)  # type: ignore
    return stage
