import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    response = await async_client.post('/auth/register', json={
        'email': 'catdog@mail.ru',
        'password': 'catdog'
    })

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    response = await async_client.post('/auth/register', json={
        'email': 'macho@mail.ru',
        'password': 'catdog'
    })

    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize('room_id, date_from, date_to, status_code', [
    (1, "2024-06-25", "2024-07-25", 200),
    #(7, "2024-06-26", "2024-08-28", 409)
])
async def test_get_booking(room_id, date_from, date_to, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post(
        '/bookings',
        params={'room_id': room_id, 'date_from': date_from, 'date_to': date_to}
    )

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    assert response.status_code == status_code


