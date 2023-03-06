from pydantic import BaseModel


class Task(BaseModel):
    name: str
    description: str
    hot: bool = False
    completed: bool = False
    public: bool = True


class User(BaseModel):
    username: str
    password: str
