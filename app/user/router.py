from fastapi import APIRouter, Depends, Response

from app.exceptions import (IncorrectEmailOrPasswordException,
                            UserAlreadyExistsException)
from app.models.models import UserModel
from app.secure.auth import authenticate_user
from app.secure.hash import get_password_hash
from app.secure.tokens import create_access_token
from app.user.dependencies import get_current_user, get_current_user_is_admin
from app.user.schemas import SUserAuth
from app.user.service import UserService

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(email=user_data.email, hashed_password=hashed_password)
    return {'success': 'registration done'}


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('access_token', access_token, httponly=True)
    return {'access_token': access_token}


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('access_token')
    return {'success': 'log outed'}


@router.get('/profile')
async def read_profile(current_user: UserModel = Depends(get_current_user)):
    return current_user.email, current_user.id


@router.get('/admin')
async def read_users(current_user: UserModel = Depends(get_current_user_is_admin)):
    if current_user.is_admin:
        return await UserService.find_all()