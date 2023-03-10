import uuid
import bcrypt
from pydantic import BaseModel
from sqlalchemy import MetaData, Integer, String, Table, Column, Identity, Boolean
from db import db

metadata = MetaData()

tasks = Table(
    'tasks',
    metadata,
    Column('id', Integer, Identity(start=0, cycle=False, minvalue=0), primary_key=True),
    Column('name', String, nullable=False),
    Column('description', String, nullable=False),
    Column('user', String, nullable=False),
    Column('hot', Boolean, nullable=False, default=False),
    Column('completed', Boolean, nullable=False, default=False),
    Column('public', Boolean, nullable=False, default=False),
)

users = Table(
    'users',
    metadata,
    Column('id', String, primary_key=True),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False)
)


class TaskData(BaseModel):
    token: str
    task_id: str


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

    @classmethod
    async def get_by_user(cls, user_id: str):
        query = tasks.select().where(tasks.c.user == user_id)
        fetched_tasks = await db.fetch_all(query)
        return fetched_tasks

    @classmethod
    async def get_all(cls):
        query = tasks.select().where(tasks.c.public == True)
        fetched_tasks = await db.fetch_all(query)
        return fetched_tasks

    @classmethod
    async def remove_by_id(cls, task_id: int):
        query = tasks.delete().where(tasks.c.id == task_id)
        result = await db.execute(query)
        return result

    @classmethod
    async def put(cls, **task):
        query = tasks.update(values=task).where(tasks.c.id == task.get('id'))
        result = await db.execute(query)
        return result


class ModelUser:
    @classmethod
    async def create(cls, **user):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(user['password'].encode('utf-8'), salt)
        user['password'] = hashed.decode()
        user['id'] = str(uuid.uuid4())
        query = users.insert().values(**user)
        user_id = await db.execute(query)
        return user_id

    @classmethod
    async def get_by_id(cls, user_id: str):
        query = users.select().where(users.c.id == user_id)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def get_by_username(cls, username: str):
        query = users.select().where(users.c.username == username)
        user = await db.fetch_one(query)
        return user
