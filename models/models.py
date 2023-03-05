from datetime import datetime
import bcrypt
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

users = Table(
    'users',
    metadata,
    Column('id', Integer, Identity(start=0, cycle=False, minvalue=0), primary_key=True),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False)
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


class ModelUser:
    @classmethod
    async def create(cls, **user):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(user['password'].encode('utf-8'), salt)
        user['password'] = hashed.decode()
        query = users.insert().values(**user)
        user_id = await db.execute(query)
        return user_id

    @classmethod
    async def get(cls, username):
        query = users.select().where(users.c.username == username)
        user = await db.fetch_one(query)
        return user
