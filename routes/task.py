from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from models.models import ModelTask
from schema import Task
from utils.auth import get_current_user

router = APIRouter(
    tags=['task']
)


@router.post('/task/create')
async def create_task(task: Task, token: str):
    user = await get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    task_id = await ModelTask.create(**task.dict())
    return task_id


@router.get('/task')
async def get_task(task_id: int):
    task = await ModelTask.get_by_id(task_id)
    return task
