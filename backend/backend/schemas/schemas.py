from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
import uuid


class Stages(Enum):
    NEW = "new"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
    ERROR = "error"
    TIMEOUT = "timeout"


class TaskIn(BaseModel):
    files: List[str]
    callback_url: Optional[str]
    status: Stages = Stages.NEW


class Task(TaskIn):
    id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True
