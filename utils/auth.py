from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from starlette import status

from config import SECRET_KEY, ALGORITHM
from models.models import ModelUser

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT",
    auto_error=True,
)


class TokenData(BaseModel):
    username: str | None = None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f'payloadkey: {payload} {token}')
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await ModelUser.get_by_id(username)
    if user is None:
        print(f'credentialskey: {username} {user}')
        raise credentials_exception
    return username
