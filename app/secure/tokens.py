from datetime import datetime, timedelta, timezone

from jose import jwt

from config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.RANDOM_KEY, settings.ALGORITHM
    )
    return encoded_jwt
