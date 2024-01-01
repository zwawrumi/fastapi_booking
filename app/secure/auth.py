from pydantic import EmailStr

from app.exceptions import UserNotFoundException
from app.secure.hash import verify_password
from app.user.service import UserService


async def authenticate_user(email: EmailStr, password: str):
    user = await UserService.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        raise UserNotFoundException
    return user
