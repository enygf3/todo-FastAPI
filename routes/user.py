from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from models.models import ModelUser
from schema import User
from utils.hashing import verify_password, create_access_token

router = APIRouter(
    tags=['user']
)


@router.post('/register')
async def register_user(user: User):
    user_id = await ModelUser.create(**user.dict())
    return user_id


@router.post('/login')
async def login_user(user: User = Depends()):
    user_db = await ModelUser.get(user.username)
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    if not verify_password(user.password, user_db['password']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    return create_access_token(user_db['username'])
