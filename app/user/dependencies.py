from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.exceptions import (IncorrectRoleAdmin, IncorrectRoleBoss,
                            IncorrectTokenException, TokenAbsentException,
                            TokenExpireException)
from app.models.models import UserModel
from app.user.service import UserService
from config import settings


def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.RANDOM_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenException

    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpireException

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await UserService.find_by_id(int(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


async def get_current_user_is_admin(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_admin:
        raise IncorrectRoleAdmin
    return current_user


async def get_current_user_is_boss(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_boss:
        raise IncorrectRoleBoss
    return current_user
