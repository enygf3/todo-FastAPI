from fastapi import FastAPI

from db import db
from routes.user import router as user_router
from routes.task import router as task_router

app = FastAPI(
    title='Todo'
)

app.include_router(user_router)
app.include_router(task_router)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}

