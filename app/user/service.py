from app.models.models import PortalRole, UserModel
from app.service.base import BaseService


class UserService(BaseService):
    model = UserModel

    @classmethod
    async def add(cls, email: str, hashed_password: str, roles: list[str] = None, **kwargs):
        if roles is None:
            roles = [PortalRole.ROLE_USER]

        await super(UserService, cls).add(email=email, hashed_password=hashed_password, roles=roles, **kwargs)
