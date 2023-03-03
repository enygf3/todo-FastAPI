from datetime import datetime
# import bcrypt
from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Table, Column, Identity
from db import db

metadata = MetaData()


tasks = Table(
    'tasks',
    metadata,
    Column('id', Integer, Identity(start=0, cycle=False, minvalue=0), primary_key=True),
    Column('name', String, nullable=False),
    Column('description', String, nullable=False),
)


class ModelTask:
    @classmethod
    async def create(cls, **task):
        query = tasks.insert().values(**task)
        task_id = await db.execute(query)
        return task_id

    @classmethod
    async def get_by_id(cls, task_id: int):
        query = tasks.select().where(tasks.c.id == task_id)
        task = await db.fetch_one(query)
        return task
