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
    urls: List[str]
    callback_url: Optional[str]


class TaskOnlyHash(BaseModel):
    archive_hash: uuid.UUID


class TaskOnlyStatus(BaseModel):
    status: Stages


class TaskCompleted(BaseModel):
    status: Stages
    url: str


class Task(TaskIn):
    archive_hash: uuid.UUID
    created_at: datetime
    modified_at: datetime
    status: Stages = Stages.NEW
    url: Optional[str]

    class Config:
        orm_mode = True
