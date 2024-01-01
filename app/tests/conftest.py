import asyncio
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert

from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.models.models import BookingModel, HotelModel, RoomModel, UserModel
from config import settings


@pytest.fixture(scope='function', autouse=True)
async def prepare_db():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_csv(model: str):
        with open(f'app/tests/{model}.json', 'r', encoding='utf-8') as csvfile:
            reader = json.load(csvfile)
            if model == 'users':
                for user in reader:
                    user.setdefault('roles', ['ROLE_USER'])
            return reader

    hotels = open_csv('hotels')
    rooms = open_csv('rooms')
    users = open_csv('users')
    bookings = open_csv('bookings')

    for booking in bookings:
        booking['date_from'] = datetime.strptime(booking['date_from'], '%Y-%m-%d')
        booking['date_to'] = datetime.strptime(booking['date_to'], '%Y-%m-%d')

    async with async_session_maker() as session:
        add_hotels = insert(HotelModel).values(hotels)
        add_rooms = insert(RoomModel).values(rooms)
        add_users = insert(UserModel).values(users)
        add_bookings = insert(BookingModel).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


# @pytest.fixture(scope='session')
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope='function')
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='function')
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        response = await ac.post('/auth/login', json={
            'email': 'firstuser@user.ru',
            'password': 'hashed_password_1',
        })
        print(response.text)

        assert response.status_code == 200
        yield ac

