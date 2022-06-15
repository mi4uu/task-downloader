from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
import uuid


class Stages(str, Enum):
    NEW = "new"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    TIMEOUT = "timeout"


class TaskIn(BaseModel):
    files: List[str]
    callback_url: Optional[str]


class Task(TaskIn):
    id: uuid.UUID
    created_at: datetime
    modified_at: datetime
    status: Stages = Stages.NEW
    download_url: Optional[str]

    class Config:
        orm_mode = True
