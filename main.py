from fastapi import FastAPI

from db import db
from models.models import ModelTask
from schema import Task

app = FastAPI(
    title='Todo'
)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/task/create')
async def create_task(task: Task):
    task_id = await ModelTask.create(**task.dict())
    return task_id


@app.get('/task')
async def create_task(task_id: int):
    task = await ModelTask.get_by_id(task_id)
    return task
