from fastapi import APIRouter

from models.models import ModelTask
from schema import Task

router = APIRouter(
    tags=['task']
)


@router.post('/task/create')
async def create_task(task: Task):
    task_id = await ModelTask.create(**task.dict())
    return task_id


@router.get('/task')
async def get_task(task_id: int):
    task = await ModelTask.get_by_id(task_id)
    return task
