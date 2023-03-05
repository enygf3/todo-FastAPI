from fastapi import APIRouter

from models.models import ModelUser
from schema import User

router = APIRouter(
    tags=['user']
)


@router.post('/register')
async def register_user(user: User):
    user_id = await ModelUser.create(**user.dict())
    return user_id


@router.get('/login')
async def login_user(user: User):
    pass
