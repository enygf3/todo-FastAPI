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
async def get_task(task_id: int, token: str):
    user = await get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    task = await ModelTask.get_by_id(task_id)
    return task


@router.get('/{user_id}/tasks')
async def get_user_tasks(user_id: str, token: str):
    user = await get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    tasks = await ModelTask.get_by_user(user_id)
    return tasks


@router.get('/tasks')
async def get_all_tasks(token: str):
    user = await get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    tasks = await ModelTask.get_all()
    return tasks
