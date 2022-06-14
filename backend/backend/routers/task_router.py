from fastapi import APIRouter, Depends
from backend.schemas import schemas
from backend import dal

from backend.db.database import get_db

router = APIRouter()


@router.post("/")
async def read_root(task: schemas.TaskIn, db = Depends(get_db)):
    result = await dal.create_task(db, task)
    return result
 