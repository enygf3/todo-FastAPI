from pydantic import BaseModel


class Task(BaseModel):
    name: str
    description: str

class User(BaseModel):
    username: str
    password: str
