from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from models.models import ModelTask
from schema import Task
from utils.auth import get_current_user

router = APIRouter(
    tags=['task']
)


@router.post('/task/create')
async def create_task(token: str, task: Task = Depends(get_current_user)):
    user_id = await get_current_user(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    updated_task = task.dict()
    updated_task.update({
        'user': user_id
    })
    task_id = await ModelTask.create(**updated_task)
    return task_id


@router.get('/task')
async def get_task(task_id: int = Depends(get_current_user)):
    task = await ModelTask.get_by_id(task_id)
    return task


@router.get('/{user_id}/tasks')
async def get_user_tasks(user_id: str = Depends(get_current_user)):
    tasks = await ModelTask.get_by_user(user_id)
    return tasks


@router.get('/tasks')
async def get_all_tasks(token: str = Depends(get_current_user)):
    tasks = await ModelTask.get_all()
    return tasks


@router.delete('/task')
async def delete_task_by_id(task_id: int = Depends(get_current_user)):
    try:
        result = await ModelTask.remove_by_id(task_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while deleting task"
        )
    return result


@router.put('/task')
async def patch_task(task_id: int = Depends(get_current_user), info: Task = Depends(get_current_user)):
    updated_task = info.dict()
    updated_task.update({
        'id': task_id
    })
    try:
        result = await ModelTask.put(**updated_task)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while updating task"
        )
    return 'Successfully updated'
