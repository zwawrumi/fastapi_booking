import pytest

from app.user.service import UserService


@pytest.mark.parametrize('user_id, email, is_present', [
    (1, 'firstuser@user.ru', True),
    (2, 'seconduser@user.ru', True),
    (3, 'macho@mail.ru', False),
    (4, 'email', False),
])
async def test_find_by_id(user_id, email, is_present):
    user = await UserService.find_by_id(user_id)
    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
